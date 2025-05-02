# FAA Special Conditions Template Filler Documentation

## Quick Links
- [Installation](installation.md)
- [User Guide](user_guide.md)
- [Developer Guide](dev_guide.md)
- [Error Reference](errors.md)

## Installation

```bash
pip install -e .
```

## Usage

### Command Line Interface

Basic usage with input files in root directory:
```bash
# Process worksheet and save output
faa-sc-filler \
    --template templates/SC_Notice_Template.docx \
    --worksheet input/SC_worksheet.docx \
    --output output/processed_SC.docx

# Preview changes without saving (dry run)
faa-sc-filler \
    --template templates/SC_Notice_Template.docx \
    --worksheet input/SC_worksheet.docx \
    --dry-run

# Custom missing field token
faa-sc-filler \
    --template templates/SC_Notice_Template.docx \
    --worksheet input/SC_worksheet.docx \
    --need-token "[[MISSING:" \
    --output output/processed_SC.docx

# Debug logging
faa-sc-filler \
    --template templates/SC_Notice_Template.docx \
    --worksheet input/SC_worksheet.docx \
    --log-level DEBUG \
    --output output/processed_SC.docx
```

### Web Interface

Start the Gradio web interface:
```bash
python -m faa_sc_filler.webui
```

Then open your browser to http://localhost:7860 and:
1. Upload template DOCX file
2. Upload worksheet DOCX file
3. Click "Generate" to process
4. Download the result

## Project Structure
```
/workspaces/FAASpecialConditionTemplateFiller/
├── src/               # Source code
├── tests/            # Test files
├── templates/        # Template DOCX files
├── input/           # Input worksheet files
├── output/          # Generated output files
└── docs/            # Documentation
```

For more details, see the specific documentation sections linked above.