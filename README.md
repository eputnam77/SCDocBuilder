# FAA Special Conditions Template Filler

Tool for automating FAA Special Conditions document generation.

[Full documentation](docs/README.md)

## Installation

```bash
pip install -r requirements.txt
```

## Quick Start

```bash
faa-sc-filler --template templates/SC_Notice_Template.docx \
    --worksheet input/SC_worksheet.docx
```

The processed document will be saved to the `output/` directory by default if no
output path is provided.

## Streamlit Interface

For a simple web UI run:

```bash
python -m faa_sc_filler.streamlit_app
```

Upload the template and worksheet files, then click **Generate** to download the
result.
