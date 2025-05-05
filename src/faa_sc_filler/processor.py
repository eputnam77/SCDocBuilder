import logging
from typing import Dict, Optional, Union, Tuple, Any
from docx import Document
from docx.document import Document as DocumentType
from .config import EXIT_SUCCESS, EXIT_REPLACEMENT_ERROR
from .replacer import PlaceholderReplacer
from .extractor import WorksheetExtractor
from .validator import DocumentValidator

logger = logging.getLogger(__name__)

class DocumentProcessor:
    """Orchestrates document processing operations."""
    
    def __init__(self):
        logger.debug("Initializing DocumentProcessor")
        self.extractor = WorksheetExtractor()
        self.replacer = PlaceholderReplacer()
        self.validator = DocumentValidator()
        self.replacements = {}
    
    def process_document(self, template: Union[str, DocumentType], 
                        replacements: Dict[str, str], 
                        output_path: Optional[str] = None,
                        dry_run: bool = False) -> Tuple[Optional[str], Optional[Dict]]:
        """Process document with replacements."""
        logger.debug(f"Starting document processing with dry_run={dry_run}")
        logger.debug(f"Replacements: {replacements}")
        
        if dry_run:
            # Build diff dictionary for dry run
            diff = {}
            for key, value in replacements.items():
                logger.debug(f"Adding diff entry: {key} -> {value}")
                diff[key] = {"old": key, "new": value}
            return None, diff
            
        try:
            # Convert Document to path if needed
            template_path = template if isinstance(template, str) else output_path
            
            # Always use PlaceholderReplacer's process_document
            self.replacer.process_document(
                template_path=template_path,
                replacements=replacements,
                output_path=output_path
            )
            
            return output_path, None
            
        except Exception as e:
            logger.error(f"Error processing document: {str(e)}")
            raise

# Keep the standalone process_document function for backwards compatibility
def process_document(template_path: str, replacements: Dict[str, str], output_path: str) -> int:
    """Process document replacing placeholders with values."""
    logger.debug("Starting document processing...")
    try:
        replacer = PlaceholderReplacer()
        replacer.process_document(template_path, replacements, output_path)
        return EXIT_SUCCESS
    except Exception as e:
        logger.error(f"Error processing document: {str(e)}")
        return EXIT_REPLACEMENT_ERROR
