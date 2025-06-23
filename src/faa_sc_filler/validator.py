import os
import re
import logging
from typing import List, Dict
from zipfile import ZipFile, BadZipFile
from .config import DEFAULT_CONFIG

logger = logging.getLogger(__name__)


class DocumentValidator:
    """Validates input files, content, and field formats."""

    VALID_CFR_PARTS = {"23", "25", "27", "29", "31", "33", "35"}

    def __init__(self):
        logger.debug("Initializing DocumentValidator")

    @staticmethod
    def validate_docx(
        filepath: str, max_size: int = DEFAULT_CONFIG["max_file_size"]
    ) -> bool:
        """Check if file is valid DOCX."""
        logger.debug(f"Validating DOCX file: {filepath}")
        logger.debug(f"Max size allowed: {max_size/1024/1024}MB")

        if not os.path.exists(filepath):
            logger.error(f"File not found: {filepath}")
            raise FileNotFoundError(f"File not found: {filepath}")

        file_size = os.path.getsize(filepath)
        logger.debug(f"File size: {file_size/1024/1024:.2f}MB")

        if file_size > max_size:
            logger.error(f"File too large: {file_size/1024/1024:.2f}MB")
            raise ValueError(f"File too large (>{max_size/1024/1024}MB): {filepath}")

        try:
            with ZipFile(filepath) as zf:
                has_content = "[Content_Types].xml" in zf.namelist()
                logger.debug(f"DOCX validation result: {has_content}")
                return has_content
        except BadZipFile:
            logger.error(f"Invalid DOCX file: {filepath}")
            raise ValueError(f"Not a valid DOCX file: {filepath}")

    @staticmethod
    def validate_required_fields(
        content: Dict[str, str], required: List[str] = None
    ) -> List[str]:
        """Return list of missing required fields."""
        logger.debug(f"Validating required fields: {required}")
        logger.debug(f"Content keys: {list(content.keys())}")

        if required is None:
            required = [
                "Applicant",
                "Model",
                "Summary",
                "Description",
                "SpecialConditions",
            ]
            logger.debug(f"Using default required fields: {required}")

        missing = [
            field
            for field in required
            if not content.get(field) or not content.get(field).strip()
        ]
        logger.debug(f"Missing required fields: {missing}")
        return missing

    @staticmethod
    def validate_cfr_part(value: str) -> bool:
        """Validate CFR part numbers."""
        logger.debug(f"Validating CFR part: {value}")
        parts = {p.strip() for p in value.split(",")}
        logger.debug(f"Parsed parts: {parts}")
        result = all(p in DocumentValidator.VALID_CFR_PARTS for p in parts)
        logger.debug(f"CFR validation result: {result}")
        return result

    @staticmethod
    def validate_docket_no(value: str) -> bool:
        """Validate docket number format."""
        logger.debug(f"Validating docket number: {value}")
        result = bool(re.match(r"^FAA-\d{4}-\d{4}$", value))
        logger.debug(f"Docket number validation result: {result}")
        return result

    @staticmethod
    def validate_notice_no(value: str) -> bool:
        """Validate notice number format."""
        logger.debug(f"Validating notice number: {value}")
        result = bool(re.match(r"^\d{2}-\d{2}-\d{2}-SC$", value))
        logger.debug(f"Notice number validation result: {result}")
        return result

    @staticmethod
    def validate_date(value: str) -> bool:
        """Validate date format (YYYY-MM-DD)."""
        logger.debug(f"Validating date: {value}")
        result = bool(
            re.match(r"^\d{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\d|3[01])$", value)
        )
        logger.debug(f"Date validation result: {result}")
        return result

    def prompt_for_missing_fields(
        self, extracted_data: Dict[str, str]
    ) -> Dict[str, str]:
        """Prompt user for missing required fields."""
        logger.debug("Prompting for missing fields")
        logger.debug(f"Current extracted data: {extracted_data}")

        if not extracted_data.get("{CFRPart}"):
            logger.debug("CFR Part is missing")
            while True:
                value = input(
                    f"Enter CFR Part(s) (comma-separated - {','.join(sorted(self.VALID_CFR_PARTS))}): "
                )
                logger.debug(f"User input for CFR Part: {value}")
                if self.validate_cfr_part(value):
                    extracted_data["{CFRPart}"] = value
                    logger.debug(f"Valid CFR Part set: {value}")
                    break
                logger.debug(f"Invalid CFR Part input: {value}")
                print(
                    "Invalid CFR Part(s). Please use valid numbers separated by commas."
                )

        if not extracted_data.get("{DocketNo}"):
            logger.debug("Docket No. is missing")
            while True:
                value = input("Enter Docket No. (format: FAA-YYYY-XXXX): ")
                logger.debug(f"User input for Docket No.: {value}")
                if self.validate_docket_no(value):
                    extracted_data["{DocketNo}"] = value
                    logger.debug(f"Valid Docket No. set: {value}")
                    break
                logger.debug(f"Invalid Docket No. input: {value}")
                print("Invalid format. Use FAA-YYYY-XXXX format.")

        if not extracted_data.get("{NoticeNo}"):
            logger.debug("Notice No. is missing")
            while True:
                value = input("Enter Notice No. (format: XX-XX-XX-SC): ")
                logger.debug(f"User input for Notice No.: {value}")
                if self.validate_notice_no(value):
                    extracted_data["{NoticeNo}"] = value
                    logger.debug(f"Valid Notice No. set: {value}")
                    break
                logger.debug(f"Invalid Notice No. input: {value}")
                print("Invalid format. Use XX-XX-XX-SC format.")

        logger.debug(f"Final extracted data after prompts: {extracted_data}")
        return extracted_data
