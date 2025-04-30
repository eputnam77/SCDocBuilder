# Error Codes & Troubleshooting

## Exit Codes
- `0`: Success
- `1`: File not found
- `2`: Validation error
- `3`: Replacement error

## Common Issues

### File Validation Errors
- File too large (>10MB)
- Invalid DOCX format
- Missing required fields

### Placeholder Issues
- Split placeholders across runs
- Malformed placeholder syntax
- Missing field values

## Logging

Log files are stored in:
- CLI: `~/.local/share/faa-sc-filler/logs/`
- Web: `<app_dir>/logs/`
