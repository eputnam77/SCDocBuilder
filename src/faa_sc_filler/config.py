from typing import Dict, List

# Field mappings for worksheet extraction
_RAW_FIELD_MAPPINGS: Dict[str, str] = {
    "14 CFR Part": "{CFRPart}",
    "Docket No.": "{DocketNo}",
    "Notice No.": "{NoticeNo}",
    "Final Notice No.": "{FinalNoticeNo}",
    "Name of Modifier": "{Modifier}",
    "Applicant name": "{ApplicantName}",
    "Airplane manufacturer": "{AirplaneManufacturer}",
    "Airplane model": "{AirplaneModel}",
    "Derivative model (if applicable)": "{Derivative}",
    "Subject of special conditions": "{SubjectOfSC}",
    "CPN project number": "{CPN}",
    "Date of application": "{ApplicationDate}",
    "Anticipated certification date": "{CertDate}",
    "certification date": "{CertDate}",
    "Anticipated delivery date": "{DeliveryDate}",
    "Type of airplane: transport category, freighter, VIP, business jet, etc.": "{AirplaneType}",
    "Number of engines (twin-engine, etc.)": "{NumberEngines}",
    "Maximum passenger capacity of all listed aircraft": "{PassengerCapacity}",
    "Maximum takeoff weight of all listed aircraft": "{TakeoffWeight}",
    "TC number (does not apply to new TC project)": "{TCNumber}",
    "TC number": "{TCNumber}",
    "Name of SME": "{SMEName}",
    "Section name": "{SMESection}",
    "Routing symbol": "{SMERoutingSymbol}",
    "SME Regional Office address": "{SMEROAddress}",
    "Telephone phone no": "{SMEPhone}",
    "E-mail": "{SMEEmail}",
    "Briefly (one to three sentences) provide a summary of the novel or unusual design features of the airplane.": "{Summary}",
    "Provide a detailed discussion of the special conditions.": "{Description}",
    "Provide the text of the special conditions.": "{SpecialConditions}",
    "6. Check the appropriate box and complete": "{ProjectType}",
}


def _normalize(key: str) -> str:
    import re

    key = key.strip()
    key = re.sub(r"^[a-z]\.|^[0-9]+\.", "", key, flags=re.IGNORECASE).strip()
    return key.rstrip(":")


FIELD_MAPPINGS: Dict[str, str] = {
    _normalize(name): placeholder for name, placeholder in _RAW_FIELD_MAPPINGS.items()
}

CHECKBOX_MAPPINGS = {
    "☒ This is a new TC project": "new TC",
    "☒ This is an amended TC project": "amended TC",
    "☒ This is a change": "change",
    "☒ This is an STC project": "STC",
}

MULTILINE_FIELDS: List[str] = [
    "Provide a detailed discussion of the special conditions.",
    "Briefly (one to three sentences) provide a summary of the novel or unusual design features of the airplane.",
    "Provide the text of the special conditions.",
    "14 CFR Part",  # In case CFR part needs multiline handling
    "TC number",  # Handle TC number as multiline to capture value on next line
    "TC number (does not apply to new TC project)",  # Handle TC number variations
    "e. TC number (does not apply to new TC project)",
]

# Default configuration
DEFAULT_CONFIG = {
    "need_token": "[[NEED:",
    "max_file_size": 10 * 1024 * 1024,  # 10MB
    "log_level": "INFO",
}

# Exit codes
EXIT_SUCCESS = 0
EXIT_FILE_NOT_FOUND = 1
EXIT_VALIDATION_ERROR = 2
EXIT_REPLACEMENT_ERROR = 3
