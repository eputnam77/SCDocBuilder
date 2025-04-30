# FAA Special Conditions Template Filler - User Guide

## Command Line Usage

```bash
python -m faa_sc_filler --template template.docx --worksheet input.docx
```

### Options
- `--output`: Specify output filename
- `--dry-run`: Preview changes without saving
- `--need-token`: Custom token for missing fields (default: [[NEED:]])

## Web Interface

1. Open the Gradio interface
2. Upload template and worksheet files
3. Click "Generate" to process
4. Download the result or view diff preview

## Troubleshooting

### Common Issues
- Missing fields are marked with [[NEED:field]]
- File size limit: 10MB
- Supported format: DOCX only
