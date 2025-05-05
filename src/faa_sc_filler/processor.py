import logging
import re
from typing import Dict, Optional, Union, Tuple, Any
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
        logger.debug("Initializing DocumentProcessor")
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
            logger.debug("Processing section headers and footers")
            # Process header
            if section.header:
                logger.debug("Processing header")
                for paragraph in section.header.paragraphs:
                    logger.debug(f"Processing header paragraph: {paragraph.text}")
                    for run in paragraph.runs:
                        original_text = run.text
                        for key, value in self.replacements.items():
                            if key in original_text:
                                logger.debug(f"Replacing {key} with {value} in header")
                                run.text = original_text.replace(key, value)
            
            # Process footer using same logic as header
            if section.footer:
                logger.debug("Processing footer")
                for paragraph in section.footer.paragraphs:
                    logger.debug(f"Processing footer paragraph: {paragraph.text}")
                    for run in paragraph.runs:
                        original_text = run.text
                        for key, value in self.replacements.items():
                            if key in original_text:
                                logger.debug(f"Replacing {key} with {value} in footer")
                                run.text = original_text.replace(key, value)
    
    def _process_header_footer(self, section: Section) -> None:
        """Process headers and footers in a section."""
        if section.header:
            for paragraph in section.header.paragraphs:
                self.replacer.process_paragraph(paragraph, self.replacements)
        if section.footer:
            for paragraph in section.footer.paragraphs:
                self.replacer.process_paragraph(paragraph, self.replacements)
    
    def process_conditional_blocks(self, doc: DocumentType, selected_option: Optional[int] = None) -> None:
        logger.debug(f"Processing conditional blocks with selected option: {selected_option}")
        paragraphs_to_remove = []
        current_option = None
        
        for i, paragraph in enumerate(doc.paragraphs):
            text = paragraph.text
            logger.debug(f"Checking paragraph {i}: {text[:50]}...")
            
            # Check for option start
            if "[[OPTION_" in text:
                current_option = int(text[text.find("_")+1:text.find("]")])
                logger.debug(f"Found option start: {current_option}")
                if selected_option and current_option != selected_option:
                    logger.debug(f"Marking option {current_option} for removal")
                    paragraphs_to_remove.append(i)
            # Check for option end
            elif "[[/OPTION_" in text:
                if current_option and current_option != selected_option:
                    paragraphs_to_remove.append(i)
                current_option = None
        
        logger.debug(f"Paragraphs marked for removal: {paragraphs_to_remove}")
        # Remove paragraphs in reverse order to maintain indices
        for idx in reversed(paragraphs_to_remove):
            logger.debug(f"Removing paragraph at index {idx}")
            p = doc.paragraphs[idx]._element
            p.getparent().remove(p)

    def process_table(self, table: Table) -> None:
        logger.debug("Processing table for replacements")
        for row_idx, row in enumerate(table.rows):
            for cell_idx, cell in enumerate(row.cells):
                logger.debug(f"Processing cell [{row_idx}][{cell_idx}]")
                logger.debug(f"Cell text before processing: {cell.text}")
                modified_text = cell.text
                for key, value in self.replacements.items():
                    if key in modified_text:
                        modified_text = modified_text.replace(key, value)
                cell.text = modified_text
                logger.debug(f"Cell text after processing: {cell.text}")

    def process_summary_paragraph(self, paragraph: Paragraph) -> None:
        logger.debug(f"Processing summary paragraph: {paragraph.text[:50]}...")
        if not paragraph.text.strip().startswith("SUMMARY:"):
            logger.debug("Not a summary paragraph, skipping")
            return
            
        # Store original content and clear paragraph
        original_text = paragraph.text
        logger.debug(f"Original text: {original_text}")
        paragraph.clear()
        
        # Add "SUMMARY: " in bold
        summary_header = paragraph.add_run("SUMMARY: ")
        summary_header.bold = True
        logger.debug(f"Added summary header with bold={summary_header.bold}")
        
        # Process the remaining content
        content_text = original_text[8:].strip()  # Remove "SUMMARY:"
        logger.debug(f"Content text before processing: {content_text}")
        
        # Process replacements
        for key, value in self.replacements.items():
            if key in content_text:
                content_text = content_text.replace(key, value)
                logger.debug(f"Replaced {key} with {value}")
        
        # Force content to use sentence case
        words = content_text.split()
        if words:
            words[0] = words[0].capitalize()  # First word capitalized
            content_text = ' '.join(words)
        logger.debug(f"Processed content text: {content_text}")
        
        # Add content without bold
        content = paragraph.add_run(content_text)
        content.bold = False
        logger.debug(f"Final run content: '{content.text}', bold={content.bold}")

    def process_document(self, template: Union[str, DocumentType], 
                        replacements: Dict[str, str], 
                        output_path: Optional[str] = None, 
                        dry_run: bool = False) -> Tuple[Optional[str], Optional[Dict]]:
        """Process document with replacements."""
        logger.debug(f"Starting document processing with dry_run={dry_run}")
        logger.debug(f"Template type: {type(template)}")
        logger.debug(f"Replacements: {replacements}")
        logger.debug(f"Output path: {output_path}")
        
        self.replacements = replacements
        doc = template if isinstance(template, DocumentType) else Document(template)
        
        if dry_run:
            # Build diff dictionary for dry run
            diff = {}
            for key, value in replacements.items():
                logger.debug(f"Adding diff entry: {key} -> {value}")
                diff[key] = {"old": key, "new": value}
            return None, diff
            
        # Process document parts
        self.process_sections(doc)
        
        # Set up regex pattern
        placeholder_pattern = re.compile(r'\{[^}]+\}')
        
        def process_paragraph_text(text: str) -> str:
            """Helper to process text and replace placeholders."""
            modified_text = text
            placeholders = placeholder_pattern.findall(text)
            for placeholder in placeholders:
                if placeholder in replacements:
                    logger.debug(f"Replacing placeholder {placeholder} with {replacements[placeholder]}")
                    modified_text = modified_text.replace(placeholder, replacements[placeholder])
                else:
                    field_name = placeholder.strip('{}')
                    logger.debug(f"Placeholder {placeholder} not found in replacements, marking as need token")
                    modified_text = modified_text.replace(placeholder, f"{self.need_token}{field_name}]]")
            return modified_text
        
        # Process all paragraphs
        for paragraph in doc.paragraphs:
            logger.debug(f"Processing paragraph: {paragraph.text[:50]}...")
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
                        logger.debug(f"Processing table cell: {cell.text[:50]}...")
                        modified_text = process_paragraph_text(cell.text)
                        cell.text = modified_text
        
        if output_path:
            doc.save(output_path)
            logger.debug(f"Document saved to {output_path}")
            return output_path, None
            
        return None, None

    def process_document(self, template: Document, replacements: Dict[str, str], output_path: Optional[str] = None, dry_run: bool = False) -> Tuple[Optional[str], Dict[str, Any]]:
        logger.debug(f"Starting document processing with dry_run={dry_run}")
        logger.debug(f"Template type: {type(template)}")
        logger.debug(f"Replacements: {replacements}")
        logger.debug(f"Output path: {output_path}")
        
        diff = {}
        doc = template
        
        # Create set of found tokens for tracking missing ones
        found_tokens = set()
        
        for paragraph in doc.paragraphs:
            self._process_paragraph(paragraph, replacements, diff, found_tokens)
            
        # Check for missing required tokens
        required_tokens = {
            "{CFRPart}", "{DocketNo}", "{NoticeNo}", "{ApplicantName}", 
            "{AirplaneManufacturer}", "{AirplaneModel}", "{SubjectOfSC}",
            "{ApplicationDate}", "{CertDate}", "{TCNumber}"
        }
        
        # Mark missing tokens in diff
        for token in required_tokens:
            if token not in found_tokens:
                if token not in replacements or not replacements[token].strip():
                    diff[token] = {
                        "old": token,
                        "new": f"NEED: {token[1:-1]}"  # Remove braces for cleaner display
                    }
                    replacements[token] = f"NEED: {token[1:-1]}"

        if not dry_run and output_path:
            doc.save(output_path)
            logger.debug(f"Document saved to {output_path}")
            return output_path, diff
        return None, diff

    def _process_paragraph(self, paragraph, replacements: Dict[str, str], diff: Dict[str, Any], found_tokens: set):
        """Process a paragraph for replacements and track found tokens."""
        content = paragraph.text
        logger.debug(f"Processing paragraph: {content[:50]}...")
        
        # Find all tokens in the paragraph
        tokens = re.findall(r'\{[^}]+\}', content)
        found_tokens.update(tokens)
        
        for token in tokens:
            old_value = token
            new_value = replacements.get(token, f"NEED: {token[1:-1]}")  # Remove braces for cleaner display
            
            if token in replacements:
                if not replacements[token].strip():  # Check if value is empty or whitespace
                    new_value = f"NEED: {token[1:-1]}"
                    
            # Record the change
            diff[token] = {
                "old": old_value,
                "new": new_value
            }
            
            # Replace in paragraph
            for run in paragraph.runs:
                run.text = run.text.replace(token, new_value)
