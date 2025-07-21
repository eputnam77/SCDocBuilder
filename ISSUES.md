# Test Results

- **Lock check**: `poetry check --lock` succeeded but `pip-compile --dry-run` failed (command not found).
- **Type checking**: `mypy` reported no issues.
- **Tests**: failed during collection due to missing dependency `docx`; coverage not generated.
- **Coverage HTML**: not generated; `gh` CLI not found so artifact upload skipped.

Test suite failed; see logs. 
