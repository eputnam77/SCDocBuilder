import os
import logging
from typing import List, Dict
from zipfile import ZipFile, BadZipFile
from .config import DEFAULT_CONFIG

logger = logging.getLogger(__name__)

class DocumentValidator:
    """Validates input files and content."""
    
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
        return [field for field in required if not content.get(field)]
