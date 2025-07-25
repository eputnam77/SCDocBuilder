"""Command-line interface for the Special Condition Template Filler."""

from __future__ import annotations

import argparse
import json
import logging
from logging.handlers import RotatingFileHandler
import sys
from enum import IntEnum
from datetime import datetime
from pathlib import Path

from . import processing
from .io import load_document, save_document, validate_input_files
from .validation import validate_mandatory_fields
from .config import load_placeholder_schema


class ErrorCode(IntEnum):
    """Numeric exit codes for common error categories."""

    OK = 0
    ENOFILE = 1
    EVALID = 2
    EREPLACE = 3


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--template", required=True, help="Path to template .docx")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--worksheet", help="Path to worksheet .docx")
    group.add_argument(
        "--batch",
        help="Directory containing worksheet .docx files",
    )
    parser.add_argument("--output", help="Output path for processed document")
    parser.add_argument(
        "--schema", help="Path to placeholder schema JSON or YAML", default=None
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Print JSON diff without saving"
    )
    parser.add_argument("--html-out", help="Save sanitized HTML to this path")
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
    handlers: list[logging.Handler] = [
        logging.StreamHandler(),
        RotatingFileHandler(
            "scdocbuilder.log", maxBytes=5 * 1024 * 1024, backupCount=2
        ),
    ]
    logging.basicConfig(
        level=getattr(logging, args.log_level),
        handlers=handlers,
        force=True,
    )
    template = Path(args.template)
    schema = load_placeholder_schema(Path(args.schema)) if args.schema else None

    try:
        if args.batch:
            batch_dir = Path(args.batch)
            if not batch_dir.is_dir():
                raise FileNotFoundError(str(batch_dir))
            output_dir = Path(args.output) if args.output else batch_dir
            output_dir.mkdir(parents=True, exist_ok=True)
            for worksheet in batch_dir.glob("*.docx"):
                validate_input_files(template, worksheet)
                template_doc = load_document(template)
                worksheet_doc = load_document(worksheet)
                validate_mandatory_fields(worksheet_doc)

                values = processing.extract_fields(worksheet_doc, schema)
                processing.replace_placeholders(template_doc, values)
                processing.apply_conditionals(template_doc, values)

                output = (
                    output_dir / f"{worksheet.stem}_{datetime.now():%Y%m%d_%H%M%S}.docx"
                ).resolve()

                if args.dry_run:
                    diff = {k: {"old": k, "new": v} for k, v in values.items()}
                    print(json.dumps(diff, indent=2))
                else:
                    save_document(template_doc, output)
                    print(str(output))
        else:
            worksheet = Path(args.worksheet)

            validate_input_files(template, worksheet)

            template_doc = load_document(template)
            worksheet_doc = load_document(worksheet)
            validate_mandatory_fields(worksheet_doc)

            values = processing.extract_fields(worksheet_doc, schema)
            processing.replace_placeholders(template_doc, values)
            processing.apply_conditionals(template_doc, values)

            output = (
                Path(args.output).resolve()
                if args.output
                else Path(
                    f"{template.stem}_{datetime.now():%Y%m%d_%H%M%S}.docx"
                ).resolve()
            )

            if args.dry_run:
                diff = {k: {"old": k, "new": v} for k, v in values.items()}
                print(json.dumps(diff, indent=2))
            else:
                save_document(template_doc, output)
                print(str(output))
                if args.html_out:
                    from .html_export import export_html

                    html = export_html(template_doc)
                    Path(args.html_out).write_text(html, encoding="utf-8")
    except FileNotFoundError as exc:
        logging.error(str(exc))
        sys.exit(ErrorCode.ENOFILE)
    except ValueError as exc:
        logging.error(str(exc))
        sys.exit(ErrorCode.EVALID)
    except Exception as exc:  # pragma: no cover - unexpected errors
        logging.exception("Processing failed", exc_info=exc)
        sys.exit(ErrorCode.EREPLACE)


if __name__ == "__main__":
    main()
