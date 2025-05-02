import os
import re
import logging
from typing import List, Dict, Optional
from zipfile import ZipFile, BadZipFile
from .config import DEFAULT_CONFIG

logger = logging.getLogger(__name__)

class DocumentValidator:
    """Validates input files, content, and field formats."""
    
    VALID_CFR_PARTS = {"23", "25", "27", "29", "31", "33", "35"}
    
    @staticmethod
    def validate_docx(filepath: str, max_size: int = DEFAULT_CONFIG["max_file_size"]) -> bool:
        """Check if file is valid DOCX."""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")
            
        if os.path.getsize(filepath) > max_size:
            raise ValueError(f"File too large (>{max_size/1024/1024}MB): {filepath}")
            
        try:
            with ZipFile(filepath) as zf:
                return "[Content_Types].xml" in zf.namelist()
        except BadZipFile:
            raise ValueError(f"Not a valid DOCX file: {filepath}")
    
    @staticmethod
    def validate_required_fields(content: Dict[str, str], required: List[str] = None) -> List[str]:
        """Return list of missing required fields."""
        if required is None:
            required = ["Applicant", "Model", "Summary", "Description", "SpecialConditions"]
        return [field for field in required if not content.get(field) or not content.get(field).strip()]

    @staticmethod
    def validate_cfr_part(value: str) -> bool:
        """Validate CFR part numbers."""
        parts = {p.strip() for p in value.split(",")}
        return all(p in DocumentValidator.VALID_CFR_PARTS for p in parts)

    @staticmethod
    def validate_docket_no(value: str) -> bool:
        """Validate docket number format."""
        return bool(re.match(r'^FAA-\d{4}-\d{4}$', value))

    @staticmethod
    def validate_notice_no(value: str) -> bool:
        """Validate notice number format."""
        return bool(re.match(r'^\d{2}-\d{2}-\d{2}-SC$', value))

    @staticmethod
    def validate_date(value: str) -> bool:
        """Validate date format (YYYY-MM-DD)."""
        return bool(re.match(r'^\d{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\d|3[01])$', value))

    def prompt_for_missing_fields(self, extracted_data: Dict[str, str]) -> Dict[str, str]:
        """Prompt user for missing required fields."""
        if not extracted_data.get("{CFRPart}"):
            while True:
                value = input(f"Enter CFR Part(s) (comma-separated - {','.join(sorted(self.VALID_CFR_PARTS))}): ")
                if self.validate_cfr_part(value):
                    extracted_data["{CFRPart}"] = value
                    break
                print("Invalid CFR Part(s). Please use valid numbers separated by commas.")

        if not extracted_data.get("{DocketNo}"):
            while True:
                value = input("Enter Docket No. (format: FAA-YYYY-XXXX): ")
                if self.validate_docket_no(value):
                    extracted_data["{DocketNo}"] = value
                    break
                print("Invalid format. Use FAA-YYYY-XXXX format.")

        if not extracted_data.get("{NoticeNo}"):
            while True:
                value = input("Enter Notice No. (format: XX-XX-XX-SC): ")
                if self.validate_notice_no(value):
                    extracted_data["{NoticeNo}"] = value
                    break
                print("Invalid format. Use XX-XX-XX-SC format.")

        return extracted_data
