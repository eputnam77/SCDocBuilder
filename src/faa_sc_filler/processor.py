import logging
from typing import Dict, Optional, Union
from docx import Document
from docx.document import Document as DocumentType
from docx.section import Section
from docx.table import Table, _Cell
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
        for section in doc.sections:
            if section.header:
                for paragraph in section.header.paragraphs:
                    self.replacer.process_paragraph(paragraph, self.replacements)
            if section.footer:
                for paragraph in section.footer.paragraphs:
                    self.replacer.process_paragraph(paragraph, self.replacements)
    
    def _process_header_footer(self, section: Section) -> None:
        """Process headers and footers in a section."""
        if section.header:
            for paragraph in section.header.paragraphs:
                self.replacer.process_paragraph(paragraph, self.replacements)
        if section.footer:
            for paragraph in section.footer.paragraphs:
                self.replacer.process_paragraph(paragraph, self.replacements)
    
    def process_conditional_blocks(self, doc: DocumentType) -> None:
        """Process Q6 conditional blocks marked with [[OPTION_N]]."""
        # Implementation for conditional block processing
        pass

    def process_table(self, table: Table) -> None:
        """Process table cells for replacements."""
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    self.replacer.process_paragraph(paragraph, self.replacements)

    def process_document(self, template: Union[str, DocumentType], 
                        replacements: Dict[str, str], 
                        output_path: Optional[str] = None, 
                        dry_run: bool = False) -> Optional[Dict]:
        """Process document with replacements."""
        self.replacements = replacements
        
        # Handle both file paths and Document objects
        if isinstance(template, str):
            self.validator.validate_docx(template)
            doc = Document(template)
        else:
            doc = template
            
        # Process document parts
        self.process_sections(doc)
        
        # Process all paragraphs
        for paragraph in doc.paragraphs:
            self.replacer.process_paragraph(paragraph, replacements)
        
        # Process all tables
        for table in doc.tables:
            self.process_table(table)
        
        if output_path and not dry_run:
            doc.save(output_path)
            
        return None
