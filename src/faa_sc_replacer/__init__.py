"""High level API for the Special Condition template replacer."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Optional

from .io import load_document, save_document, validate_input_files
from .processing import apply_conditionals, extract_fields, replace_placeholders

__all__ = [
    "fill_template",
    "extract_fields",
    "replace_placeholders",
    "apply_conditionals",
    "load_document",
    "save_document",
    "validate_input_files",
]


def fill_template(
    template_path: Path | str,
    worksheet_path: Path | str,
    output_path: Optional[Path | str] = None,
) -> Path:
    """Fill ``template_path`` with values from ``worksheet_path``.

    The processed document is saved to ``output_path``. If none is provided a
    timestamped file is created next to the template.
    """

    template = Path(template_path)
    worksheet = Path(worksheet_path)
    validate_input_files(template, worksheet)

    template_doc = load_document(template)
    worksheet_doc = load_document(worksheet)

    values = extract_fields(worksheet_doc)
    replace_placeholders(template_doc, values)
    apply_conditionals(template_doc, values)

    if output_path is None:
        output_path = template.with_name(
            f"{template.stem}_{datetime.now():%Y%m%d_%H%M%S}.docx"
        )

    output = Path(output_path)
    save_document(template_doc, output)
    return output
