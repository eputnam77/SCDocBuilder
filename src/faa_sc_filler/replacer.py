import logging
from typing import Dict, List
from docx.text.paragraph import Paragraph
from docx.table import Table
from docx import Document

logger = logging.getLogger(__name__)

class PlaceholderReplacer:
    """Handles replacement of placeholders in Word documents."""
    
    def __init__(self):
        logger.debug("Initializing PlaceholderReplacer")
    
    def find_placeholders_in_paragraph(self, paragraph: Paragraph) -> List[str]:
        """Find all placeholders in a paragraph."""
        logger.debug(f"Finding placeholders in paragraph: '{paragraph.text[:50]}...'")
        
        text = paragraph.text
        # Look for text between curly braces
        import re
        placeholders = re.findall(r'\{[^}]+\}', text)
        
        logger.debug(f"Found placeholders: {placeholders}")
        return placeholders

    def join_split_runs(self, paragraph: Paragraph) -> None:
        """Join runs that might contain split placeholders."""
        logger.debug(f"Joining split runs in paragraph: '{paragraph.text[:50]}...'")
        logger.debug(f"Number of runs before joining: {len(paragraph.runs)}")
        
        if len(paragraph.runs) <= 1:
            logger.debug("No runs to join")
            return
            
        # Collect all text from runs
        full_text = ''.join(run.text for run in paragraph.runs)
        
        # Clear all runs except the first one
        first_run = paragraph.runs[0]
        first_run.text = full_text
        
        for run in paragraph.runs[1:]:
            run.text = ""
            
        logger.debug(f"Joined text: '{full_text[:50]}...'")
        logger.debug(f"Number of runs after joining: {len(paragraph.runs)}")

    def process_paragraph(self, paragraph: Paragraph, replacements: Dict[str, str]) -> None:
        """Process a paragraph for placeholder replacements."""
        logger.debug(f"Processing paragraph: '{paragraph.text[:50]}...'")
        logger.debug(f"Available replacements: {replacements}")

        if not paragraph.text:
            logger.debug("Empty paragraph, skipping")
            return

        text = paragraph.text
        modified = False
        logger.debug(f"Number of runs in paragraph: {len(paragraph.runs)}")
        
        # Process each run
        for i, run in enumerate(paragraph.runs):
            original_text = run.text
            run_text = original_text
            logger.debug(f"Processing run {i}: '{original_text[:50]}...'")
            
            for key, value in replacements.items():
                if key in run_text:
                    logger.debug(f"Found placeholder '{key}' in run")
                    run_text = run_text.replace(key, value)
                    logger.debug(f"Replaced with '{value}'")
                    modified = True
                    
            if modified:
                logger.debug(f"Updating run text from '{original_text[:50]}...' to '{run_text[:50]}...'")
                run.text = run_text
        
        # If no runs or no replacement in runs, handle whole paragraph
        if not modified and paragraph.runs:
            logger.debug("No modifications in individual runs, processing entire paragraph")
            modified_text = text
            for key, value in replacements.items():
                if key in modified_text:
                    logger.debug(f"Replacing {key} with {value} in whole paragraph")
                    modified_text = modified_text.replace(key, value)
            
            logger.debug(f"Setting modified text to first run: '{modified_text[:50]}...'")
            paragraph.runs[0].text = modified_text
            if len(paragraph.runs) > 1:
                logger.debug(f"Clearing {len(paragraph.runs)-1} remaining runs")
                for run in paragraph.runs[1:]:
                    run.text = ""

    def process_document(self, template_path: str, replacements: Dict[str, str], output_path: str) -> None:
        """Process the entire document for replacements."""
        logger.debug(f"Processing document: {template_path}")
        logger.debug(f"Output path: {output_path}")
        logger.debug(f"Replacements to apply: {replacements}")
        
        try:
            doc = Document(template_path)
            logger.debug("Document loaded successfully")
            
            # Process all paragraphs
            logger.debug(f"Processing {len(doc.paragraphs)} paragraphs")
            for paragraph in doc.paragraphs:
                self.process_paragraph(paragraph, replacements)
            
            # Process all tables
            logger.debug(f"Processing {len(doc.tables)} tables")
            for table in doc.tables:
                for row in table.rows:
                    for cell in row.cells:
                        for paragraph in cell.paragraphs:
                            self.process_paragraph(paragraph, replacements)
            
            # Process headers and footers in all sections
            logger.debug("Processing headers and footers")
            for section in doc.sections:
                if section.header:
                    for paragraph in section.header.paragraphs:
                        self.process_paragraph(paragraph, replacements)
                if section.footer:
                    for paragraph in section.footer.paragraphs:
                        self.process_paragraph(paragraph, replacements)
            
            # Save the processed document
            logger.debug(f"Saving document to: {output_path}")
            doc.save(output_path)
            logger.info("Document processing completed successfully")
            
        except Exception as e:
            logger.error(f"Error processing document: {str(e)}")
            raise
