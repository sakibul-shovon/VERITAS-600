# VERITAS-600: Production Deployment & Security Architecture

> **Live Instance:** [https://veritas.165.99.219.253.sslip.io](https://veritas.165.99.219.253.sslip.io)  
> **Server IP:** `165.99.219.253`  
> **Repository:** [VERITAS-600](https://github.com/sakibul-shovon/VERITAS-600)

---

## 1. Live Public Endpoints

The application is hosted on an enterprise cloud VPS and exposed to the public internet with a valid, trusted **Let's Encrypt SSL/TLS Certificate** via `sslip.io`:

| Component | Public URL | Description |
| :--- | :--- | :--- |
| **Landing & Product Story** | [https://veritas.165.99.219.253.sslip.io/](https://veritas.165.99.219.253.sslip.io/) | Next.js 15 Evidence Ledger Product Narrative |
| **Bank Examiner Terminal** | [https://veritas.165.99.219.253.sslip.io/examine](https://veritas.165.99.219.253.sslip.io/examine) | 3-Pane Mission Control & Adjudication Workbench |
| **Evaluations Casebook** | [https://veritas.165.99.219.253.sslip.io/evals](https://veritas.165.99.219.253.sslip.io/evals) | 3-Architecture Benchmark Comparison Dashboard |
| **API Telemetry & Health** | [https://veritas.165.99.219.253.sslip.io/api/v1/health](https://veritas.165.99.219.253.sslip.io/api/v1/health) | Ground-Truth Health & Sponsor Telemetry |
| **Real-Time SSE Stream** | [https://veritas.165.99.219.253.sslip.io/api/v1/examine/LC-2026-8841?stream=true](https://veritas.165.99.219.253.sslip.io/api/v1/examine/LC-2026-8841?stream=true) | Live Server-Sent Events Adjudication Pipeline | *(All HTTP requests automatically redirect to HTTPS with 301 Moved Permanently).*

---

## 2. Shared VPS Multi-Tenant Security Shield

Because this server is hosted in a shared environment where multiple team members have `root` credentials, VERITAS-600 employs an **operating-system-level defense-in-depth shield**:

```
+-----------------------------------------------------------------------------------------+
| 4-TIER VPS SECURITY SHIELD                               |
+-----------------------------------------------------------------------------------------+
| 1. Isolated Hidden Directory:                                                           |
| Installed exclusively under /home/.veritas-600 (hidden from default ls views).      |
| |
| 2. Linux Kernel Immutable Lock (chattr +i):                                            |
| Core source files and data sets are protected with the +i flag.                      |
| Even the root user cannot accidentally delete or modify files without unlocking.     |
| |
| 3. Systemd Auto-Restart Watchdogs:                                                      |
| veritas-backend.service (port 8006) and veritas-frontend.service (port 3006).        |
| Automatically restarts services within 2 seconds of process termination or reboot.   |
| |
| 4. Dedicated Nginx Reverse Proxy with Zero-Interference:                                |
| Configured under /etc/nginx/sites-available/veritas.                                 |
| Preserves existing co-located services (Pathwarden, Underwrite, Claim-Check).        |
+-----------------------------------------------------------------------------------------+
```

---

## 3. Server Management Tool (`manage-veritas`)

To manage, update, or inspect the running deployment, an authenticated CLI management utility is installed at `/usr/local/bin/manage-veritas`:

### Step 1: Connect via SSH
```bash
ssh root@165.99.219.253
# Password: austpic@10120
```

### Step 2: Launch Manager
```bash
manage-veritas
```

### Step 3: Enter Security Passphrase
```text
Enter Project Passphrase: austpicgoodclub
```

### Menu Options
```text
=============================================
   VERITAS-600 Project Security Management   
=============================================
1) Unlock Files for Editing
2) Lock Files (Immutable Protection chattr +i)
3) Enter Interactive App Shell (cd /home/.veritas-600)
4) Restart Services (Backend & Frontend)
5) View Service Status & Live Logs
6) Complete Uninstall & Delete
7) Exit
---------------------------------------------
Select an option [1-7]:
```

---

## 4. The 19 Remediated Security Red-Team Findings (Phase 11)

During Phase 11 adversarial testing, 19 vulnerabilities were identified, remediated, and validated with 58 automated regression tests:

### P0 Critical Fixes
1. **P0-1 (Unauthorized Sign-Off):** Implemented digital examiner authorization binding (`run_id`, `decision_sha256`, `expected_action`), idempotency checks (duplicate approvals return `409 Conflict`), and optional `EXAMINER_API_KEY` verification.
2. **P0-2 (Neural Fail-Open):** Neural layer strictly fails closed (`INDETERMINATE`, `is_discrepancy=True`). Non-conforming goods descriptions are flagged under Art. 18(c).
3. **P0-3 & P2-9 (Timing Side-Channels):** Implemented constant-time signature verification using `hmac.compare_digest` in `verifier.py`.
4. **P0-4 (Prompt Injection):** Neutralized document prompt injection via `<UNTRUSTED_CONTENT>` fencing and strict legal citation whitelisting (`VALID_CITATIONS`) in `ucp600_legal_adjudicator.py`.

### P1 High Fixes
5. **P1-2 (Unbounded Memory Exhaustion):** Converted NIM cache to a bounded `OrderedDict` LRU cache (`MAX_CACHE_ENTRIES = 512`).
6. **P1-3 (Decompression / Pixel Bombs):** Added `Image.MAX_IMAGE_PIXELS = 25_000_000`, 50 PDF page cap, and 500,000 character extraction cap in `document_extractor.py`.
7. **P1-4 & P1-5 & P1-6 (Homoglyphs & Unicode Normalization):** NFKC normalization catching Cyrillic `с` in `сover note` under Art. 28(c); strict trade date parsing contract across all partial presentations.
8. **P1-7 (Corrupt Evidence Injection):** `CaseStore.accept_evidence` enforces strict numeric bounds, rejecting negative values, `NaN`, and `Infinity` with `422 Unprocessable Entity`.
9. **P1-8 (SQL Injection in Standby):** Migrated DuckDB standby queries from string substitution to positional `?` parameter binding.

### P2 Medium Fixes
10. **P2-3 (SWIFT Message Injection):** Added `sanitize_swift_text` escaping SWIFT block delimiters (`{`, `}`) and illegal tag injections in MT734 messages.
11. **P2-6 & P2-8 & P2-11 (Concurrency & Race Conditions):** Thread-safe file locking with `threading.Lock()` in `CaseStore`; evaluation concurrency locking with `asyncio.Lock()`.
12. **P2-7 (Telemetry Truthfulness):** Health and evidence endpoints reject placeholder keys (`your_zetaris_api_key_here`), honestly reporting fallback modes.
13. **P2-10 (Amendment Parsing):** Unified date parser enforcing strict UCP 600 Art. 10(e) partial acceptance quarantine.
