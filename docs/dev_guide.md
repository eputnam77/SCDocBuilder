# Developer Guide

## Architecture

The application follows a modular design with these key components:

- `extractor.py`: Worksheet data extraction
- `replacer.py`: Placeholder replacement logic
- `processor.py`: Document-wide processing
- `validator.py`: Input validation
- `cli.py`: Command-line interface
- `webui.py`: Gradio web interface
- `ai_editor.py`: Optional AI editorial review helpers

## Module Dependencies
```mermaid
graph TD
    A[cli.py] --> B[processor.py]
    C[webui.py] --> B
    B --> D[extractor.py]
    B --> E[replacer.py]
    B --> F[validator.py]
```

## Configuration
See `config.py` for customizable settings:
- Field mappings
- Logging configuration
- File size limits
- Need tokens
