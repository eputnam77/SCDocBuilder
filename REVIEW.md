# Review of recent changes

## PRD Compliance

- **F1–F5, F7–F9** implemented: CLI enforces required `--template` and worksheet/batch flags with optional `--output`, `--schema`, `--dry-run`, `--html-out`, and logging options【F:src/scdocbuilder/cli.py†L39-L57】. When `--output` is omitted the program saves to `{template-stem}_{timestamp}.docx`【F:src/scdocbuilder/cli.py†L131-L137】. Placeholder values are extracted from paragraphs and tables and replacements cover text boxes, tables, headers, and footers with conditional blocks handled via a precompiled regex【F:src/scdocbuilder/processing.py†L81-L109】【F:src/scdocbuilder/processing.py†L121-L148】. `--dry-run` emits a JSON diff, and errors return explicit exit codes【F:src/scdocbuilder/cli.py†L139-L141】【F:src/scdocbuilder/cli.py†L20-L26】【F:src/scdocbuilder/cli.py†L150-L170】.
- **F6** unmet: HTML export simply escapes text and omits the required `mammoth` + `bleach` sanitisation【F:src/scdocbuilder/html_export.py†L1-L28】.
- Validation only checks file extension and size; MIME verification from the PRD is missing【F:src/scdocbuilder/io.py†L25-L31】.

## Integration

- Unit tests: 24 failed / 39 passed; most failures arise because the local `docx` stub lacks file-path loading, causing `TypeError` during document operations【d834d0†L1-L22】【F:src/docx/document.py†L73-L75】【F:src/scdocbuilder/io.py†L44-L45】.
- Property and e2e tests are skipped, leaving key paths untested【825b4f†L1-L3】【82c6da†L1-L3】.
- Bandit, Semgrep, pytest-cov, and mutmut could not run—dependencies unavailable in the current environment.

## Performance

- Conditional block regex is compiled once at import to avoid repetitive cost【F:src/scdocbuilder/processing.py†L22-L23】. The `benchmark_processing` helper times document loading, but failing tests prevent verifying the ≤1 s requirement.

## Maintainability

- Repository uses a custom `docx` stub whose API diverges from `python-docx`, breaking real document handling and tests【F:src/docx/document.py†L73-L79】.
- `export_html` lacks true sanitisation, risking unsanitised HTML output【F:src/scdocbuilder/html_export.py†L1-L28】.

## Blocking Issues 🔴

1. Custom `docx` stub incompatible with `python-docx`, leading to failing tests and unusable document IO【F:src/docx/document.py†L73-L79】【F:src/scdocbuilder/io.py†L44-L45】.
2. F6 (TipTap HTML export) unfulfilled; HTML output is not sanitised【F:src/scdocbuilder/html_export.py†L1-L28】.
3. File validation omits MIME checking contrary to PRD requirements【F:src/scdocbuilder/io.py†L25-L31】.
4. YAML schema loading requires optional PyYAML dependency; tests fail when absent【d834d0†L10】.
5. Security and quality tools (Bandit, Semgrep, coverage, mutation) not executed.

## Info Comments 🟢

- Regex precompilation for conditionals is good; consider similar optimisations for other heavy patterns【F:src/scdocbuilder/processing.py†L22-L23】.
- Provide offline caches or bundled wheels so Bandit/Semgrep/pytest-cov/mutmut can run without network access.
- Expand README with contribution guidelines and examples for broader developer uptake.

_Label: `ready-for:builder`_
