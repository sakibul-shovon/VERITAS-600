"""Multimodal Document Extraction Engine (VLM / OCR).

Extracts structured trade finance fields, spatial bounding boxes [ymin, xmin, ymax, xmax],
and cryptographic source digests from rendered documents and presentations.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
from io import BytesIO
import json
from pathlib import Path
import re
from typing import Any, Dict, List, Optional

from PIL import Image
from pypdf import PdfReader

try:  # PyMuPDF enables page rendering and exact boxes; text PDFs still work without it.
    import fitz
except ImportError:  # pragma: no cover - platform wheel compatibility is environment-specific.
    fitz = None

try:  # Portable fallback for scanned-PDF rendering when PyMuPDF is unavailable.
    import pypdfium2 as pdfium
except ImportError:  # pragma: no cover - dependency availability is environment-specific.
    pdfium = None

from apps.api.inference.nim_client import NvidiaNimClient

ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent
PRESENTATIONS_DIR = ROOT_DIR / "data" / "presentations"


@dataclass
class ExtractedField:
    field_key: str
    value: Any
    confidence: float
    bounding_box: List[int]  # [ymin, xmin, ymax, xmax] in normalized 0-1000 scale
    source_document: str
    source_digest_sha256: str = ""
    page_number: int = 1


@dataclass
class DocumentExtractionResult:
    document_type: str
    document_id: str
    fields: Dict[str, ExtractedField]
    raw_text: str
    extraction_mode: str  # 'LIVE_NEMOTRON_VLM', 'CACHED_REPLAY', or 'STRUCTURED_FIXTURE'
    source_digest_sha256: str = ""
    notice: str = ""


class DocumentExtractor:
    """Multimodal document extractor utilizing Nemotron Vision with honest telemetry and fallbacks."""

    def __init__(self, nim_client: Optional[NvidiaNimClient] = None):
        self.nim_client = nim_client or NvidiaNimClient()

    def _load_presentation_context(self, lc_id: str) -> Dict[str, Any]:
        """Load document context for an LC if available."""
        file_path = PRESENTATIONS_DIR / f"{lc_id}.json"
        if file_path.exists():
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def extract_document(
        self,
        document_type: str,
        document_text_or_path: str,
        lc_id: str,
        presentation_data: Optional[Dict[str, Any]] = None,
    ) -> DocumentExtractionResult:
        """Extract structured fields with coordinates from document text/scan."""
        context = presentation_data or self._load_presentation_context(lc_id)
        master = context.get("master", {})
        presentation = context.get("presentation", {})

        doc_type_upper = document_type.upper()
        raw_source = f"{document_type}:{lc_id}:{json.dumps(context, sort_keys=True)}"
        source_digest = hashlib.sha256(raw_source.encode("utf-8")).hexdigest()

        # Determine extraction mode truthfully:
        # Only claim LIVE_NEMOTRON_VLM if live API call is executed and succeeds
        extraction_mode = "STRUCTURED_FIXTURE"

        if "INVOICE" in doc_type_upper:
            return self._extract_commercial_invoice(lc_id, master, presentation, source_digest, extraction_mode)
        elif "BILL OF LADING" in doc_type_upper or "B/L" in doc_type_upper:
            return self._extract_ocean_bill_of_lading(lc_id, master, presentation, source_digest, extraction_mode)
        elif "PACKING" in doc_type_upper:
            return self._extract_packing_list(lc_id, master, presentation, source_digest, extraction_mode)
        elif "INSURANCE" in doc_type_upper:
            return self._extract_insurance_document(lc_id, master, presentation, source_digest, extraction_mode)

        # Default extraction
        return DocumentExtractionResult(
            document_type=document_type,
            document_id=f"DOC-{lc_id}",
            fields={},
            raw_text=document_text_or_path,
            extraction_mode=extraction_mode,
            source_digest_sha256=source_digest,
        )

    def extract_uploaded_document(
        self,
        document_type: str,
        filename: str,
        content_type: str,
        content: bytes,
        lc_id: str,
    ) -> DocumentExtractionResult:
        """Extract from real uploaded bytes without silently substituting fixture data."""
        digest = hashlib.sha256(content).hexdigest()
        normalized_type = document_type.strip().lower()
        display_type = {
            "commercial_invoice": "Commercial Invoice",
            "bill_of_lading": "Ocean Bill of Lading",
            "packing_list": "Packing List",
            "insurance": "Insurance Document",
        }.get(normalized_type, "Other Document")

        if content_type == "application/pdf" or filename.lower().endswith(".pdf"):
            pdf = None
            try:
                if fitz is not None:
                    pdf = fitz.open(stream=content, filetype="pdf")
                    pages = [page.get_text("text").strip() for page in pdf]
                else:
                    reader = PdfReader(BytesIO(content))
                    pages = [(page.extract_text() or "").strip() for page in reader.pages]
                raw_text = "\n\n".join(text for text in pages if text)
            except Exception as exc:
                return self._unavailable_result(display_type, filename, digest, f"Invalid PDF: {type(exc).__name__}")
            if len(raw_text) >= 20:
                fields = self._extract_fields_from_text(normalized_type, raw_text, pdf, digest, display_type)
                if pdf is not None:
                    pdf.close()
                return DocumentExtractionResult(
                    document_type=display_type,
                    document_id=f"UPLOAD-{digest[:16]}",
                    fields=fields,
                    raw_text=raw_text[:20000],
                    extraction_mode="PDF_TEXT_LAYER",
                    source_digest_sha256=digest,
                    notice="Fields were derived from the uploaded PDF text layer and require examiner review.",
                )
            images = self._render_pdf_content(content, pdf)
            if not images:
                return self._unavailable_result(
                    display_type,
                    filename,
                    digest,
                    "This appears to be a scanned PDF; page rendering is unavailable in this runtime.",
                )
            if pdf is not None:
                pdf.close()
            return self._extract_with_vision(display_type, filename, normalized_type, digest, images)

        if content_type in {"image/png", "image/jpeg", "image/jpg", "image/webp"}:
            try:
                image = self._compress_image(content)
            except Exception as exc:
                return self._unavailable_result(display_type, filename, digest, f"Invalid image: {type(exc).__name__}")
            return self._extract_with_vision(display_type, filename, normalized_type, digest, [("image/jpeg", image)])

        return self._unavailable_result(display_type, filename, digest, "Only PDF, PNG, JPEG, or WebP evidence is supported.")

    def _unavailable_result(self, document_type: str, filename: str, digest: str, notice: str) -> DocumentExtractionResult:
        return DocumentExtractionResult(
            document_type=document_type,
            document_id=f"UPLOAD-{digest[:16]}",
            fields={},
            raw_text="",
            extraction_mode="OCR_UNAVAILABLE",
            source_digest_sha256=digest,
            notice=notice,
        )

    def _render_pdf_pages(self, pdf: Any) -> List[tuple[str, bytes]]:
        images: List[tuple[str, bytes]] = []
        for page in list(pdf)[:3]:
            pixmap = page.get_pixmap(matrix=fitz.Matrix(1.6, 1.6), alpha=False)
            images.append(("image/jpeg", self._compress_image(pixmap.tobytes("png"))))
        return images

    def _render_pdf_content(self, content: bytes, fitz_pdf: Any = None) -> List[tuple[str, bytes]]:
        if fitz_pdf is not None:
            return self._render_pdf_pages(fitz_pdf)
        if pdfium is None:
            return []
        document = pdfium.PdfDocument(content)
        images: List[tuple[str, bytes]] = []
        try:
            for page_index in range(min(len(document), 3)):
                page = document[page_index]
                rendered = page.render(scale=1.6).to_pil()
                output = BytesIO()
                rendered.save(output, format="PNG")
                images.append(("image/jpeg", self._compress_image(output.getvalue())))
                page.close()
        finally:
            document.close()
        return images

    def _compress_image(self, content: bytes) -> bytes:
        image = Image.open(BytesIO(content)).convert("RGB")
        image.thumbnail((1600, 1600))
        quality = 82
        while True:
            output = BytesIO()
            image.save(output, format="JPEG", quality=quality, optimize=True)
            encoded = output.getvalue()
            if len(encoded) <= 175_000 or quality <= 42:
                return encoded
            quality -= 10

    def _extract_with_vision(
        self,
        document_type: str,
        filename: str,
        normalized_type: str,
        digest: str,
        images: List[tuple[str, bytes]],
    ) -> DocumentExtractionResult:
        requested_fields = {
            "commercial_invoice": ["invoice_no", "invoice_date", "applicant", "goods_description", "unit_price", "total_amount"],
            "bill_of_lading": ["bl_no", "vessel", "goods_description", "on_board_date", "gross_weight", "notify_party"],
            "packing_list": ["packing_gross_weight"],
            "insurance": ["insurance_doc_type", "insurance_amount", "effective_date"],
        }.get(normalized_type, [])
        prompt = (
            "Extract documentary-credit evidence from the supplied pages. Return JSON only with "
            "shape {\"raw_text\": string, \"fields\": {key: {\"value\": scalar, "
            "\"confidence\": number from 0 to 1, \"page_number\": integer, "
            "\"bounding_box\": [ymin,xmin,ymax,xmax] normalized 0-1000}}}. "
            f"Document type: {document_type}. Required keys when present: {requested_fields}. "
            "Do not infer missing values and do not add legal conclusions."
        )
        response = self.nim_client.complete_multimodal(prompt, images)
        if response.get("telemetry") == "OCR_UNAVAILABLE":
            return self._unavailable_result(document_type, filename, digest, response.get("error", "Vision OCR unavailable."))

        try:
            parsed = self._parse_json_response(response.get("content", ""))
            fields: Dict[str, ExtractedField] = {}
            for key, item in (parsed.get("fields") or {}).items():
                if requested_fields and key not in requested_fields:
                    continue
                box = item.get("bounding_box") or [0, 0, 1000, 1000]
                if len(box) != 4:
                    box = [0, 0, 1000, 1000]
                fields[key] = ExtractedField(
                    field_key=key,
                    value=item.get("value"),
                    confidence=max(0.0, min(1.0, float(item.get("confidence", 0)))),
                    bounding_box=[max(0, min(1000, int(value))) for value in box],
                    source_document=document_type,
                    source_digest_sha256=digest,
                    page_number=max(1, int(item.get("page_number", 1))),
                )
            return DocumentExtractionResult(
                document_type=document_type,
                document_id=f"UPLOAD-{digest[:16]}",
                fields=fields,
                raw_text=str(parsed.get("raw_text", ""))[:20000],
                extraction_mode=response.get("telemetry", "LIVE_UNCACHED").replace("LIVE_UNCACHED", "LIVE_NEMOTRON_VLM"),
                source_digest_sha256=digest,
                notice="Vision-extracted fields require examiner review before examination.",
            )
        except Exception as exc:
            return self._unavailable_result(document_type, filename, digest, f"Vision response was not valid structured JSON: {type(exc).__name__}")

    @staticmethod
    def _parse_json_response(content: str) -> Dict[str, Any]:
        cleaned = content.strip()
        if cleaned.startswith("```"):
            cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
            cleaned = re.sub(r"\s*```$", "", cleaned)
        return json.loads(cleaned)

    def _extract_fields_from_text(
        self,
        document_type: str,
        raw_text: str,
        pdf: Any,
        digest: str,
        display_type: str,
    ) -> Dict[str, ExtractedField]:
        patterns: Dict[str, List[tuple[str, str]]] = {
            "commercial_invoice": [
                ("invoice_no", r"(?:invoice\s*(?:no\.?|number|#)|inv\s*#)\s*[:\-]?\s*([A-Z0-9][A-Z0-9\-/]+)"),
                ("invoice_date", r"(?:invoice\s*)?date\s*[:\-]?\s*(\d{4}[-/]\d{2}[-/]\d{2}|\d{1,2}[-/]\d{1,2}[-/]\d{2,4})"),
                ("goods_description", r"(?:goods\s*description|description\s*of\s*goods)\s*[:\-]?\s*([^\n]+)"),
                ("unit_price", r"unit\s*price\s*[:\-]?\s*(?:[A-Z]{3}|[$€£])?\s*([0-9,]+(?:\.\d{1,2})?)"),
                ("total_amount", r"(?:invoice\s*amount|grand\s*total|total\s*amount)\s*[:\-]?\s*(?:[A-Z]{3}|[$€£])?\s*([0-9,]+(?:\.\d{1,2})?)"),
            ],
            "bill_of_lading": [
                ("bl_no", r"(?:b/?l|bill\s*of\s*lading)\s*(?:no\.?|number|#)?\s*[:\-]?\s*([A-Z0-9][A-Z0-9\-/]+)"),
                ("vessel", r"(?:vessel|vessel\s*name)\s*[:\-]?\s*([^\n]+)"),
                ("goods_description", r"(?:goods\s*description|description\s*of\s*goods)\s*[:\-]?\s*([^\n]+)"),
                ("on_board_date", r"(?:on[- ]board\s*date|shipped\s*on\s*board)\s*[:\-]?\s*(\d{4}[-/]\d{2}[-/]\d{2}|\d{1,2}[-/]\d{1,2}[-/]\d{2,4})"),
                ("gross_weight", r"gross\s*weight\s*[:\-]?\s*([0-9,]+(?:\.\d+)?)"),
                ("notify_party", r"notify\s*party\s*[:\-]?\s*([^\n]+)"),
            ],
            "packing_list": [("packing_gross_weight", r"gross\s*weight\s*[:\-]?\s*([0-9,]+(?:\.\d+)?)")],
            "insurance": [
                ("insurance_doc_type", r"(insurance\s*(?:certificate|policy)|cover\s*note)"),
                ("insurance_amount", r"(?:insured\s*amount|sum\s*insured|amount)\s*[:\-]?\s*(?:[A-Z]{3}|[$€£])?\s*([0-9,]+(?:\.\d{1,2})?)"),
                ("effective_date", r"(?:effective\s*date|risk\s*commencement)\s*[:\-]?\s*(\d{4}[-/]\d{2}[-/]\d{2}|\d{1,2}[-/]\d{1,2}[-/]\d{2,4})"),
            ],
        }
        numeric_fields = {"unit_price", "total_amount", "gross_weight", "packing_gross_weight", "insurance_amount"}
        fields: Dict[str, ExtractedField] = {}
        for key, pattern in patterns.get(document_type, []):
            match = re.search(pattern, raw_text, flags=re.IGNORECASE)
            if not match:
                continue
            value: Any = match.group(1).strip()
            if key in numeric_fields:
                value = float(value.replace(",", ""))
            page_number, box = self._locate_text(pdf, match.group(1).strip())
            fields[key] = ExtractedField(
                field_key=key,
                value=value,
                confidence=0.98,
                bounding_box=box,
                source_document=display_type,
                source_digest_sha256=digest,
                page_number=page_number,
            )
        return fields

    @staticmethod
    def _locate_text(pdf: Any, value: str) -> tuple[int, List[int]]:
        if pdf is None:
            return 1, [0, 0, 1000, 1000]
        for page_index, page in enumerate(pdf):
            rectangles = page.search_for(value)
            if rectangles:
                rect = rectangles[0]
                width = max(page.rect.width, 1)
                height = max(page.rect.height, 1)
                return page_index + 1, [
                    round(rect.y0 / height * 1000),
                    round(rect.x0 / width * 1000),
                    round(rect.y1 / height * 1000),
                    round(rect.x1 / width * 1000),
                ]
        return 1, [0, 0, 1000, 1000]

    def _extract_commercial_invoice(
        self,
        lc_id: str,
        master: Dict[str, Any],
        presentation: Dict[str, Any],
        source_digest: str,
        extraction_mode: str,
    ) -> DocumentExtractionResult:
        inv_no = presentation.get("invoice_no", f"INV-{lc_id[3:]}-01")
        inv_date = presentation.get("invoice_date", master.get("latest_shipment_date", "2026-10-14"))
        applicant = master.get("applicant_name", "Pacific Heavy Machinery Pte Ltd")
        goods_desc = presentation.get(
            "invoice_goods_description",
            master.get("goods_description_strict", "INDUSTRIAL EQUIPMENT"),
        )
        unit_price = float(presentation.get("invoice_unit_price", master.get("unit_price", 480.00)))
        total_amount = float(presentation.get("invoice_amount", master.get("amount", 240000.00)))

        fields = {
            "invoice_no": ExtractedField("invoice_no", inv_no, 0.99, [120, 750, 150, 920], "Commercial Invoice", source_digest),
            "invoice_date": ExtractedField("invoice_date", inv_date, 0.98, [160, 750, 190, 880], "Commercial Invoice", source_digest),
            "applicant": ExtractedField("applicant", applicant, 0.99, [220, 100, 260, 480], "Commercial Invoice", source_digest),
            "goods_description": ExtractedField("goods_description", goods_desc, 0.97, [450, 100, 520, 850], "Commercial Invoice", source_digest),
            "unit_price": ExtractedField("unit_price", unit_price, 0.99, [450, 700, 480, 780], "Commercial Invoice", source_digest),
            "total_amount": ExtractedField("total_amount", total_amount, 0.99, [580, 720, 620, 920], "Commercial Invoice", source_digest),
        }

        return DocumentExtractionResult(
            document_type="Commercial Invoice",
            document_id=f"INV-{lc_id}",
            fields=fields,
            raw_text=f"COMMERCIAL INVOICE {inv_no}\nApplicant: {applicant}\nAmount: {total_amount}\nGoods: {goods_desc}",
            extraction_mode=extraction_mode,
            source_digest_sha256=source_digest,
        )

    def _extract_ocean_bill_of_lading(
        self,
        lc_id: str,
        master: Dict[str, Any],
        presentation: Dict[str, Any],
        source_digest: str,
        extraction_mode: str,
    ) -> DocumentExtractionResult:
        bl_no = presentation.get("bl_no", f"MEDU-{lc_id[3:]}")
        vessel = presentation.get("bl_vessel", "EVER GLORY")
        goods_desc = presentation.get("bl_goods_description", master.get("goods_description_strict", "INDUSTRIAL EQUIPMENT"))
        on_board_date = presentation.get("bl_on_board_date", master.get("latest_shipment_date", "2026-10-16"))
        gross_weight = float(presentation.get("bl_gross_weight_kg", 18450.00))
        notify_party = presentation.get("bl_notify_party", master.get("applicant_name", ""))

        fields = {
            "bl_no": ExtractedField("bl_no", bl_no, 0.99, [80, 780, 120, 950], "Ocean Bill of Lading", source_digest),
            "vessel": ExtractedField("vessel", vessel, 0.98, [280, 100, 310, 300], "Ocean Bill of Lading", source_digest),
            "goods_description": ExtractedField("goods_description", goods_desc, 0.96, [480, 100, 530, 650], "Ocean Bill of Lading", source_digest),
            "on_board_date": ExtractedField("on_board_date", on_board_date, 0.99, [750, 600, 780, 780], "Ocean Bill of Lading", source_digest),
            "gross_weight": ExtractedField("gross_weight", gross_weight, 0.98, [480, 750, 510, 880], "Ocean Bill of Lading", source_digest),
            "notify_party": ExtractedField("notify_party", notify_party, 0.97, [220, 100, 270, 450], "Ocean Bill of Lading", source_digest),
        }

        return DocumentExtractionResult(
            document_type="Ocean Bill of Lading",
            document_id=f"BL-{lc_id}",
            fields=fields,
            raw_text=f"OCEAN BILL OF LADING {bl_no}\nVessel: {vessel}\nOn Board: {on_board_date}\nWeight: {gross_weight} KG",
            extraction_mode=extraction_mode,
            source_digest_sha256=source_digest,
        )

    def _extract_packing_list(
        self,
        lc_id: str,
        master: Dict[str, Any],
        presentation: Dict[str, Any],
        source_digest: str,
        extraction_mode: str,
    ) -> DocumentExtractionResult:
        gross_weight = float(presentation.get("packing_gross_weight_kg", 18450.00))
        fields = {
            "packing_gross_weight": ExtractedField(
                "packing_gross_weight",
                gross_weight,
                0.99,
                [460, 700, 490, 850],
                "Packing List",
                source_digest,
            ),
        }
        return DocumentExtractionResult(
            document_type="Packing List",
            document_id=f"PK-{lc_id}",
            fields=fields,
            raw_text=f"PACKING LIST FOR {lc_id}\nGross Weight: {gross_weight} KG",
            extraction_mode=extraction_mode,
            source_digest_sha256=source_digest,
        )

    def _extract_insurance_document(
        self,
        lc_id: str,
        master: Dict[str, Any],
        presentation: Dict[str, Any],
        source_digest: str,
        extraction_mode: str,
    ) -> DocumentExtractionResult:
        doc_type = presentation.get("insurance_doc_type", "Insurance Certificate")
        amount = float(presentation.get("insurance_amount", 264000.00))
        effective_date = presentation.get("insurance_effective_date", "2026-10-14")

        fields = {
            "insurance_doc_type": ExtractedField("insurance_doc_type", doc_type, 0.99, [90, 700, 130, 920], doc_type, source_digest),
            "insurance_amount": ExtractedField("insurance_amount", amount, 0.99, [520, 700, 560, 880], doc_type, source_digest),
            "effective_date": ExtractedField("effective_date", effective_date, 0.98, [210, 650, 240, 800], doc_type, source_digest),
        }

        return DocumentExtractionResult(
            document_type="Insurance Document",
            document_id=f"INS-{lc_id}",
            fields=fields,
            raw_text=f"{doc_type.upper()}\nAmount: {amount}\nEffective Date: {effective_date}",
            extraction_mode=extraction_mode,
            source_digest_sha256=source_digest,
        )
