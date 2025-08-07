# Review of recent changes

## PRD Compliance

- **F-3 unmet:** The project still uses a custom DOCX shim instead of `python-docx`, risking formatting loss and violating the requirement to use official APIs【F:src/docx/document.py†L73-L97】.
- **F-6 unmet:** HTML export manually escapes runs and omits the required `mammoth` + `bleach` sanitisation【F:src/scdocbuilder/html_export.py†L1-L37】.
- The validation layer only checks file extension and `PK` header; MIME type verification via `python-magic` is missing【F:src/scdocbuilder/io.py†L25-L34】.

## Integration

- Unit tests execute successfully with 63 passed, 8 skipped, 1 xfailed, and 1 xpassed【e7da51†L1-L2】.
- Property-based and e2e markers are present but all tests are skipped, leaving those paths unexercised【f4cbaf†L1-L3】【c0e6aa†L1-L3】.

## Performance

- `cProfile` stats are captured, yet the ≤1 s processing requirement for 500 KB + 1 MB inputs remains untested【F:.dev/PERFORMANCE_REPORT.md†L3-L5】.

## Maintainability

- Reliance on bespoke DOCX parsing increases long-term maintenance effort compared to using `python-docx`【F:src/docx/document.py†L73-L97】.
- The HTML export module’s docstring mentions libraries that are not actually used, which may mislead future contributors【F:src/scdocbuilder/html_export.py†L1-L7】.
- A lightweight YAML parser allows configuration without pulling in PyYAML, reducing dependencies for tests【F:src/scdocbuilder/config.py†L11-L27】.

## Blocking Issues 🔴

1. Replace the custom DOCX shim with `python-docx` to preserve formatting and satisfy F‑3【F:src/docx/document.py†L73-L97】.
2. Implement TipTap HTML export using `mammoth` + `bleach` as required by F‑6【F:src/scdocbuilder/html_export.py†L1-L37】.
3. Add MIME type validation with `python-magic` in `validate_input_files`【F:src/scdocbuilder/io.py†L25-L34】.

## Info Comments 🟢

- Property and E2E test markers exist but are entirely skipped; consider adding real tests before relying on those gates【f4cbaf†L1-L3】【c0e6aa†L1-L3】.
- The fallback YAML parser is a pragmatic approach that keeps tests self-contained when PyYAML is unavailable【F:src/scdocbuilder/config.py†L11-L27】.
- CLI tests inject `PYTHONPATH` to ensure modules resolve consistently across environments【F:tests/test_cli.py†L73-L87】.

_Label: `ready-for:builder`_
