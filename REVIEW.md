# Review of recent changes

## PRD Compliance

- **F6 unmet:** HTML export manually escapes runs and omits the required `mammoth` + `bleach` sanitisation despite the module docstring claiming otherwise【F:src/scdocbuilder/html_export.py†L1-L37】.
- The project still relies on a custom DOCX stub instead of `python-docx`, risking formatting loss and failing the PRD's requirement to preserve document formatting【F:src/docx/document.py†L73-L116】.
- `validate_input_files` checks for a `PK` prefix but does not verify MIME type as required by the PRD【F:src/scdocbuilder/io.py†L25-L34】.

## Integration

- Full test suite runs with 63 passed, 8 skipped, 1 xfailed, and 1 xpassed, indicating basic integration coverage【efc51c†L1-L20】.
- A lightweight YAML parser removes the hard dependency on PyYAML, allowing tests to run offline【F:src/scdocbuilder/config.py†L11-L27】【F:src/scdocbuilder/config.py†L53-L59】.

## Performance

- `cProfile` captures performance stats for the stubbed pipeline, but the ≤1 s processing requirement remains unverified【F:.dev/PERFORMANCE_REPORT.md†L1-L8】.

## Maintainability

- The bespoke DOCX format and parser increase long-term maintenance risk compared to using the standard `python-docx` library【F:src/docx/document.py†L73-L152】.
- The HTML export module's docstring mentions libraries that are not actually used, which may confuse future contributors【F:src/scdocbuilder/html_export.py†L1-L7】.

## Blocking Issues 🔴

1. Implement real TipTap HTML export via `mammoth` + `bleach` to satisfy F6【F:src/scdocbuilder/html_export.py†L1-L37】.
2. Replace the custom DOCX stub with `python-docx` to ensure formatting fidelity and reduce maintenance burden【F:src/docx/document.py†L73-L152】.
3. Add MIME type validation using `python-magic` as specified in the PRD【F:src/scdocbuilder/io.py†L25-L34】.

## Info Comments 🟢

- The fallback YAML parser is a pragmatic way to avoid extra dependencies in test environments【F:src/scdocbuilder/config.py†L11-L27】.
- Environment variable injection in CLI tests improves reproducibility across setups【F:tests/test_cli.py†L70-L87】.

_Label: `ready-for:builder`_
