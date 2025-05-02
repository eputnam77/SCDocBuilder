import logging
from typing import Dict, Optional, Union, Tuple
from docx import Document
from docx.document import Document as DocumentType
from docx.section import Section
from docx.table import Table, _Cell
from docx.text.paragraph import Paragraph
from .replacer import PlaceholderReplacer
from .extractor import WorksheetExtractor
from .validator import DocumentValidator

logger = logging.getLogger(__name__)

class DocumentProcessor:
    """Orchestrates document processing operations."""
    
    def __init__(self):
        self.extractor = WorksheetExtractor()
        self.replacer = PlaceholderReplacer()
        self.validator = DocumentValidator()
        self.replacements = {}
        self.need_token = "[[NEED:"
    
    def process_sections(self, doc: DocumentType) -> None:
        """Process headers and footers in all sections."""
        logger.debug(f"Processing document sections with replacements: {self.replacements}")
        
        # Ensure replacements is a dict
        if not isinstance(self.replacements, dict):
            logger.error(f"Invalid replacements type: {type(self.replacements)}")
            raise TypeError(f"Replacements must be a dict, not {type(self.replacements)}")
            
        for section in doc.sections:
            # Process header
            if section.header:
                for paragraph in section.header.paragraphs:
                    for run in paragraph.runs:
                        text = run.text
                        for key, value in self.replacements.items():
                            if key in text:
                                text = text.replace(key, value)
                        run.text = text
            
            # Process footer using same logic as header
            if section.footer:
                for paragraph in section.footer.paragraphs:
                    for run in paragraph.runs:
                        text = run.text
                        for key, value in self.replacements.items():
                            if key in text:
                                text = text.replace(key, value)
                        run.text = text
    
    def _process_header_footer(self, section: Section) -> None:
        """Process headers and footers in a section."""
        if section.header:
            for paragraph in section.header.paragraphs:
                self.replacer.process_paragraph(paragraph, self.replacements)
        if section.footer:
            for paragraph in section.footer.paragraphs:
                self.replacer.process_paragraph(paragraph, self.replacements)
    
    def process_conditional_blocks(self, doc: DocumentType, selected_option: Optional[int] = None) -> None:
        """Process Q6 conditional blocks marked with [[OPTION_N]].
        
        Args:
            doc: Document to process
            selected_option: Option number to keep (1-based). Others will be removed.
        """
        paragraphs_to_remove = []
        current_option = None
        
        for i, paragraph in enumerate(doc.paragraphs):
            text = paragraph.text
            
            # Check for option start
            if "[[OPTION_" in text:
                current_option = int(text[text.find("_")+1:text.find("]")])
                if selected_option and current_option != selected_option:
                    paragraphs_to_remove.append(i)
            # Check for option end
            elif "[[/OPTION_" in text:
                if current_option and current_option != selected_option:
                    paragraphs_to_remove.append(i)
                current_option = None
        
        # Remove paragraphs in reverse order to maintain indices
        for idx in reversed(paragraphs_to_remove):
            p = doc.paragraphs[idx]._element
            p.getparent().remove(p)

    def process_table(self, table: Table) -> None:
        """Process table cells for replacements."""
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    self.replacer.process_paragraph(paragraph, self.replacements)

    def process_summary_paragraph(self, paragraph: Paragraph) -> None:
        """Special handling for summary paragraph formatting."""
        if not paragraph.text.strip().startswith("SUMMARY:"):
            return
            
        # Store original text and process it
        full_text = paragraph.text
        summary_text = full_text[8:].strip()  # Remove "SUMMARY:"
        
        # Process placeholders before converting case
        processed_text = summary_text
        for key, value in self.replacements.items():
            if key in processed_text:
                processed_text = processed_text.replace(key, value)
        
        # Convert to sentence case but preserve placeholders
        processed_text = processed_text.lower()
        processed_text = processed_text[0].upper() + processed_text[1:]
        
        # Clear and rebuild paragraph with proper formatting
        for run in paragraph.runs:
            run.text = ""
            
        # Add "SUMMARY:" in bold
        summary_header = paragraph.add_run("SUMMARY: ")
        summary_header.bold = True
        
        # Add processed text without bold
        content = paragraph.add_run(processed_text)
        content.bold = False

    def process_document(self, template: Union[str, DocumentType], 
                        replacements: Dict[str, str], 
                        output_path: Optional[str] = None, 
                        dry_run: bool = False) -> Tuple[Optional[str], Optional[Dict]]:
        """Process document with replacements."""
        logger.info(f"Processing document. Dry run: {dry_run}")
        logger.debug(f"Template: {template}")
        logger.debug(f"Replacements: {replacements}")
        
        self.replacements = replacements
        doc = template if isinstance(template, DocumentType) else Document(template)
        
        if dry_run:
            # Build diff dictionary for dry run
            diff = {}
            for key, value in replacements.items():
                diff[key] = {"old": key, "new": value}
            return None, diff
            
        # Process document parts
        self.process_sections(doc)
        
        # Set up regex pattern
        import re
        placeholder_pattern = re.compile(r'\{[^}]+\}')
        
        def process_paragraph_text(text: str) -> str:
            """Helper to process text and replace placeholders."""
            modified_text = text
            placeholders = placeholder_pattern.findall(text)
            for placeholder in placeholders:
                if placeholder in replacements:
                    modified_text = modified_text.replace(placeholder, replacements[placeholder])
                else:
                    field_name = placeholder.strip('{}')
                    modified_text = modified_text.replace(placeholder, f"{self.need_token}{field_name}]]")
            return modified_text
        
        # Process all paragraphs
        for paragraph in doc.paragraphs:
            if paragraph.text.startswith("SUMMARY:"):
                self.process_summary_paragraph(paragraph)
            if placeholder_pattern.search(paragraph.text):
                modified_text = process_paragraph_text(paragraph.text)
                if paragraph.runs:
                    paragraph.runs[0].text = modified_text
                    for run in paragraph.runs[1:]:
                        run.text = ""
        
        # Process all tables
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    if placeholder_pattern.search(cell.text):
                        modified_text = process_paragraph_text(cell.text)
                        cell.text = modified_text
        
        if output_path:
            doc.save(output_path)
            return output_path, None
            
        return None, None
