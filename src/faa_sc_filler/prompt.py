from typing import Dict
from .validator import DocumentValidator

def prompt_for_missing_fields(extracted_data: Dict[str, str]) -> Dict[str, str]:
    """Prompt user for missing required fields."""
    validator = DocumentValidator()
    
    if not extracted_data.get("{CFRPart}"):
        value = input("Enter CFR Part(s) (comma-separated - 23,25,27,29,31,33,35): ")
        if not validator.validate_cfr_part(value):
            raise ValueError(f"Invalid CFR Part(s): {value}")
        extracted_data["{CFRPart}"] = value

    if not extracted_data.get("{DocketNo}"):
        while True:
            value = input("Enter Docket No. (format: FAA-YYYY-XXXX): ")
            if validator.validate_docket_no(value):
                extracted_data["{DocketNo}"] = value
                break
            print("Invalid format. Use FAA-YYYY-XXXX format.")

    if not extracted_data.get("{NoticeNo}"):
        while True:
            value = input("Enter Notice No. (format: XX-XX-XX-SC): ")
            if validator.validate_notice_no(value):
                extracted_data["{NoticeNo}"] = value
                break
            print("Invalid format. Use XX-XX-XX-SC format.")

    return extracted_data
