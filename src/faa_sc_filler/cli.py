import argparse
import logging
import os
import re
import sys
from pathlib import Path
from typing import Tuple, Optional, Dict, List
from .processor import DocumentProcessor
from .validator import DocumentValidator
from .config import DEFAULT_CONFIG
from docx import Document

logger = logging.getLogger(__name__)

# Exit codes
EXIT_SUCCESS = 0
EXIT_REPLACEMENT_ERROR = 1

def parse_args(args: Optional[List[str]] = None) -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="FAA Special Conditions Template Filler")
    parser.add_argument("--template", required=True, help="Path to template DOCX")
    parser.add_argument("--worksheet", required=True, help="Path to worksheet DOCX")
    parser.add_argument("--output", help="Output path (optional)")
    parser.add_argument("--dry-run", action="store_true", help="Show diff without saving")
    parser.add_argument("--need-token", default=DEFAULT_CONFIG["need_token"],
                      help="Token for missing fields")
    parser.add_argument("--log-level", choices=["DEBUG","INFO","WARNING","ERROR"],
                      default="INFO", help="Logging level")
    
    # Add version argument
    parser.add_argument('--version', action='version', version='%(prog)s 1.0.0')
    
    return parser.parse_args(args)

def validate_cfr_part(value: str) -> bool:
    valid_parts = {"23", "25", "27", "29", "31", "33", "35"}
    parts = {p.strip() for p in value.split(",")}
    return all(p in valid_parts for p in parts)

def validate_docket_no(value: str) -> bool:
    return bool(re.match(r'^FAA-\d{4}-\d{4}$', value))

def validate_notice_no(value: str) -> bool:
    return bool(re.match(r'^\d{2}-\d{2}-\d{2}-SC$', value))

def prompt_for_missing_fields(extracted_data: Dict[str, str]) -> Dict[str, str]:
    """Prompt user for missing required fields."""
    if not extracted_data.get("{CFRPart}"):
        while True:
            value = input("Enter CFR Part(s) (comma-separated - 23,25,27,29,31,33,35): ")
            if validate_cfr_part(value):
                extracted_data["{CFRPart}"] = value
                break
            print("Invalid CFR Part(s). Please use valid numbers separated by commas.")

    if not extracted_data.get("{DocketNo}"):
        while True:
            value = input("Enter Docket No. (format: FAA-YYYY-XXXX): ")
            if validate_docket_no(value):
                extracted_data["{DocketNo}"] = value
                break
            print("Invalid format. Use FAA-YYYY-XXXX format.")

    if not extracted_data.get("{NoticeNo}"):
        while True:
            value = input("Enter Notice No. (format: XX-XX-XX-SC): ")
            if validate_notice_no(value):
                extracted_data["{NoticeNo}"] = value
                break
            print("Invalid format. Use XX-XX-XX-SC format.")

    return extracted_data

def main(cli_args: Optional[List[str]] = None) -> int:
    """Main CLI entry point."""
    try:
        args = parse_args(cli_args)
        processor = DocumentProcessor()
        
        # Load worksheet and extract data
        worksheet_doc = Document(args.worksheet)
        worksheet_data = processor.extractor.extract_data(worksheet_doc)
        
        # Prompt for missing fields if not in dry-run mode
        if not args.dry_run:
            worksheet_data = prompt_for_missing_fields(worksheet_data)
        
        # Process the document
        processor.process_document(
            template=Document(args.template),
            replacements=worksheet_data,
            output_path=args.output,
            dry_run=args.dry_run
        )
        
        return EXIT_SUCCESS
        
    except Exception as e:
        logger.error(f"Error processing document: {e}")
        return EXIT_REPLACEMENT_ERROR

if __name__ == "__main__":
    sys.exit(main())
