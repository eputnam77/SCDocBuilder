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
    logger.debug(f"Parsing command line arguments: {args}")
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
    
    parsed_args = parser.parse_args(args)
    logger.debug(f"Parsed arguments: {vars(parsed_args)}")
    return parsed_args

def validate_cfr_part(value: str) -> bool:
    logger.debug(f"Validating CFR part: {value}")
    valid_parts = {"23", "25", "27", "29", "31", "33", "35"}
    parts = {p.strip() for p in value.split(",")}
    result = all(p in valid_parts for p in parts)
    logger.debug(f"CFR part validation result: {result}")
    return result

def validate_docket_no(value: str) -> bool:
    logger.debug(f"Validating docket number: {value}")
    result = bool(re.match(r'^FAA-\d{4}-\d{4}$', value))
    logger.debug(f"Docket number validation result: {result}")
    return result

def validate_notice_no(value: str) -> bool:
    logger.debug(f"Validating notice number: {value}")
    result = bool(re.match(r'^\d{2}-\d{2}-\d{2}-SC$', value))
    logger.debug(f"Notice number validation result: {result}")
    return result

def prompt_for_missing_fields(extracted_data: Dict[str, str]) -> Dict[str, str]:
    """Prompt user for missing required fields."""
    logger.debug("Checking for missing fields in extracted data")
    logger.debug(f"Current extracted data: {extracted_data}")

    if not extracted_data.get("{CFRPart}"):
        logger.debug("CFR Part is missing, prompting user")
        while True:
            value = input("Enter CFR Part(s) (comma-separated - 23,25,27,29,31,33,35): ")
            if validate_cfr_part(value):
                extracted_data["{CFRPart}"] = value
                logger.debug(f"CFR Part set to: {value}")
                break
            logger.debug(f"Invalid CFR Part input: {value}")
            print("Invalid CFR Part(s). Please use valid numbers separated by commas.")

    if not extracted_data.get("{DocketNo}"):
        logger.debug("Docket number is missing, prompting user")
        while True:
            value = input("Enter Docket No. (format: FAA-YYYY-XXXX): ")
            if validate_docket_no(value):
                extracted_data["{DocketNo}"] = value
                logger.debug(f"Docket number set to: {value}")
                break
            logger.debug(f"Invalid docket number input: {value}")
            print("Invalid format. Use FAA-YYYY-XXXX format.")

    if not extracted_data.get("{NoticeNo}"):
        logger.debug("Notice number is missing, prompting user")
        while True:
            value = input("Enter Notice No. (format: XX-XX-XX-SC): ")
            if validate_notice_no(value):
                extracted_data["{NoticeNo}"] = value
                logger.debug(f"Notice number set to: {value}")
                break
            logger.debug(f"Invalid notice number input: {value}")
            print("Invalid format. Use XX-XX-XX-SC format.")

    logger.debug(f"Final extracted data after prompts: {extracted_data}")
    return extracted_data

def main(cli_args: Optional[List[str]] = None) -> int:
    """Main CLI entry point."""
    try:
        logger.debug("Starting main CLI function")
        args = parse_args(cli_args)
        
        # Set up logging level
        logging.basicConfig(level=getattr(logging, args.log_level))
        logger.debug(f"Set logging level to {args.log_level}")
        
        logger.debug("Initializing DocumentProcessor")
        processor = DocumentProcessor()
        
        # Load worksheet and extract data
        logger.debug(f"Loading worksheet from: {args.worksheet}")
        worksheet_doc = Document(args.worksheet)
        logger.debug("Extracting data from worksheet")
        worksheet_data = processor.extractor.extract_data(worksheet_doc)
        logger.debug(f"Extracted worksheet data: {worksheet_data}")
        
        # Prompt for missing fields if not in dry-run mode
        if not args.dry_run:
            logger.debug("Processing missing fields")
            worksheet_data = prompt_for_missing_fields(worksheet_data)
        
        # Process the document
        logger.debug(f"Processing document with template: {args.template}")
        processor.process_document(
            template=Document(args.template),
            replacements=worksheet_data,
            output_path=args.output,
            dry_run=args.dry_run
        )
        
        logger.debug("Document processing completed successfully")
        return EXIT_SUCCESS
        
    except Exception as e:
        logger.error(f"Error processing document: {e}", exc_info=True)
        return EXIT_REPLACEMENT_ERROR

if __name__ == "__main__":
    sys.exit(main())
