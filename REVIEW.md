# Review of recent changes

## PRD Compliance

- **F-3 unmet:** The project still relies on a custom DOCX shim instead of `python-docx`, risking formatting loss and violating the requirement to use official APIs【F:src/docx/document.py†L73-L122】.
- **F-6 met:** `export_html` uses `mammoth` and `bleach` to convert and sanitise DOCX content, fulfilling the TipTap HTML export requirement【F:src/scdocbuilder/html_export.py†L23-L53】.
- MIME type validation with `python-magic` now protects against non-DOCX uploads【F:src/scdocbuilder/io.py†L34-L45】.

## Integration

- Unit tests execute successfully with 65 passed, 8 skipped, 1 xfailed, and 1 xpassed【4fdc40†L1-L20】.
- `export_html`’s unit test confirms that `mammoth` and `bleach` are invoked when present【F:tests/unit/test_html_export_mammoth.py†L14-L40】.
- MIME validation logic is covered by dedicated tests【F:tests/unit/test_io_magic.py†L9-L28】.
- Property-based tests are skipped when `hypothesis` is unavailable, leaving those paths unexercised【F:tests/property/test_processing_properties.py†L15-L18】.

## Performance

- `cProfile` stats are captured, yet the ≤1 s processing requirement for 500 KB template + 1 MB worksheet remains untested【F:.dev/PERFORMANCE_REPORT.md†L3-L5】.

## Maintainability

- Reliance on bespoke DOCX parsing continues to increase long-term maintenance effort compared to using `python-docx`【F:src/docx/document.py†L73-L122】.
- If `mammoth`, `bleach`, or `python-magic` are absent, the code silently falls back to less robust paths; packaging should ensure these dependencies are available【F:src/scdocbuilder/html_export.py†L34-L46】【F:src/scdocbuilder/io.py†L37-L45】.
- The API exposes an `html` flag that returns sanitised HTML directly, aiding integration with web clients【F:src/scdocbuilder/api.py†L72-L96】.

## Blocking Issues 🔴

1. Replace the custom DOCX shim with `python-docx` to preserve formatting and satisfy F‑3【F:src/docx/document.py†L73-L122】.

## Info Comments 🟢

- Ensure deployment packages include `mammoth`, `bleach`, and `python-magic` to avoid silently degraded functionality.
- Property and E2E test markers exist but are entirely skipped; consider adding real tests before relying on those gates【F:tests/property/test_processing_properties.py†L15-L18】.
- The API’s HTML option demonstrates the new export flow and can guide future UI integration【F:src/scdocbuilder/api.py†L72-L96】.

_Label: `ready-for:builder`_
