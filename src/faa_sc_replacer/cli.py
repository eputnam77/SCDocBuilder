"""Command-line interface for the Special Condition Template Filler."""

from __future__ import annotations

import argparse
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any

from . import processing
from .io import load_document, save_document, validate_input_files


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--template", required=True, help="Path to template .docx")
    parser.add_argument(
        "--worksheet", required=True, help="Path to worksheet .docx"
    )
    parser.add_argument("--output", help="Output path for processed document")
    parser.add_argument(
        "--dry-run", action="store_true", help="Print JSON diff without saving"
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Logging verbosity",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    """Run the placeholder replacer from the command line."""

    args = parse_args(argv)
    logging.basicConfig(level=getattr(logging, args.log_level))
    template = Path(args.template)
    worksheet = Path(args.worksheet)

    validate_input_files(template, worksheet)

    template_doc = load_document(template)
    worksheet_doc = load_document(worksheet)

    values = processing.extract_fields(worksheet_doc)
    processing.replace_placeholders(template_doc, values)
    processing.apply_conditionals(template_doc, values)

    output = (
        Path(args.output)
        if args.output
        else Path(f"{template.stem}_{datetime.now():%Y%m%d_%H%M%S}.docx")
    )

    if args.dry_run:
        diff = {k: {"old": k, "new": v} for k, v in values.items()}
        print(json.dumps(diff, indent=2))
    else:
        save_document(template_doc, output)
        print(str(output))
