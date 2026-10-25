# Launch film delivery

Research and the first review cut are complete. The film was produced after the research under the user's direct authorization. It is an original evidence-led, light-theme product film using actual running software, synthetic trade data and explicitly labelled explanatory graphics.

The local production workspace is `H:/Projects/VERITAS-600-video`. It has its own Git history and contains the editable source, capture manifest, original assets, audio stems and render scripts. The application source was not modified.

## Outputs

- `out/VERITAS-600-launch-1080p.mp4`: 174.016 seconds, 1920×1080, 30 fps, H.264/AAC, BT.709 limited range, faststart, approximately 27 MB.
- `out/review-540p.mp4`: full lightweight review proxy.
- `out/VERITAS-600-launch-1080p.srt` and `.vtt`: 50 phrase captions timed from actual generated audio sample boundaries; captions are also burned into the film.
- `out/contact-sheet.jpg` and `out/poster.jpg`: visual review artifacts.
- `qa/final-report.json`: encoded-file metadata, decode, black-frame and audio checks; a copy is [here](qa-report.json).

## Verification

Complete FFmpeg decode succeeds. No black intervals were detected. Encoded audio measures −14.10 LUFS integrated and −1.16 dBTP. Thirty representative master frames were inspected, including full-resolution opening and artifact shots. Captions are ordered, inside the runtime, and have no overlap. Independent speech recognition recovered the narration.

Product verification: 58/58 backend tests pass; Next.js production build passes with all routes generated. The repository knowledge graph was refreshed using `graphify update .`.

## Truth and remaining review

The film uses local DuckDB federation, replayed inference, local context routing, and actual text-layer PDF extraction. It does not claim a live sponsor-cloud connection. Every recommendation remains pending human sign-off. No human signature, payment, SWIFT transmission or AML filing was performed.

This is a first review cut. Automated technical checks and sampled-frame review do not replace a human listening and creative review. Commercial-studio equivalence is not independently established. Narration is synthesized; the score and sound effects are original procedural audio. The ten-case evaluation is synthetic and local/replay, not a production accuracy guarantee.

Research, tool comparisons and access limitations are in [research.md](research.md). The full feature inventory, timed storyboard and production architecture are in [production-plan.md](production-plan.md), with the exact narration in [script.json](script.json).
