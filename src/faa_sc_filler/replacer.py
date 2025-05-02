import logging
from typing import Dict, List
from docx.text.paragraph import Paragraph
from docx.table import Table

logger = logging.getLogger(__name__)

class PlaceholderReplacer:
    """Handles replacement of placeholders in Word documents."""
    
    def find_placeholders_in_paragraph(self, paragraph: Paragraph) -> List[str]:
        """Find all placeholders in a paragraph."""
        # ...existing find_placeholders_in_paragraph logic...

    def join_split_runs(self, paragraph: Paragraph) -> None:
        """Join runs that might contain split placeholders."""
        # ...existing join_split_runs logic...

    def process_paragraph(self, paragraph: Paragraph, replacements: Dict[str, str]) -> None:
        """Process a paragraph for placeholder replacements."""
        if not paragraph.text:
            return

        # Collect all runs and their text
        text = paragraph.text
        modified = False
        
        # Process each run
        for run in paragraph.runs:
            run_text = run.text
            for key, value in replacements.items():
                if key in run_text:
                    logger.debug(f"Replacing {key} with {value} in run")
                    run_text = run_text.replace(key, value)
                    modified = True
            if modified:
                run.text = run_text
        
        # If no runs or no replacement in runs, handle whole paragraph
        if not modified and paragraph.runs:
            modified_text = text
            for key, value in replacements.items():
                if key in modified_text:
                    modified_text = modified_text.replace(key, value)
            paragraph.runs[0].text = modified_text
            for run in paragraph.runs[1:]:
                run.text = ""

    def process_document(self, template_path: str, replacements: Dict[str, str], output_path: str) -> None:
        """Process the entire document for replacements."""
        # ...existing process_document logic...
