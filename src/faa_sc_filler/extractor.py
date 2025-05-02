import re
import logging
from typing import Dict, Optional, List
from docx import Document
from .config import FIELD_MAPPINGS, MULTILINE_FIELDS, CHECKBOX_MAPPINGS

logger = logging.getLogger(__name__)

class WorksheetExtractor:
    def __init__(self):
        self.field_mappings = FIELD_MAPPINGS
        self.multiline_fields = MULTILINE_FIELDS
        self.checkbox_mappings = CHECKBOX_MAPPINGS
    
    def clean_text(self, text: str) -> str:
        """Remove extra whitespace, field labels, and normalize format."""
        # Remove leading/trailing whitespace and normalize internal spaces
        text = ' '.join(text.strip().split())
        # Remove enumeration (a., b., 1., etc)
        text = re.sub(r'^[a-z0-9]\.\s*', '', text, flags=re.IGNORECASE)
        # Normalize multiple colons
        text = re.sub(r':\s*:', ':', text)
        # Normalize spaces around colons
        text = re.sub(r'\s*:\s*', ':', text)
        return text

    def extract_field_value(self, text: str, field: str) -> Optional[str]:
        """Extract field value handling various formats."""
        if not text.strip():
            return None

        # Strip all spaces around colons in both text and field
        input_text = re.sub(r'\s*:\s*', ':', text.strip())
        base_field = re.sub(r'\s*:\s*', ':', field.rstrip(':').strip())

        # Remove any enumeration prefixes for comparison
        cleaned_text = re.sub(r'^[a-z0-9]\.\s*', '', input_text, flags=re.IGNORECASE)
        cleaned_field = re.sub(r'^[a-z0-9]\.\s*', '', base_field, flags=re.IGNORECASE)

        # Get field name without the trailing colon
        field_name = cleaned_field.rstrip(':')
        
        # Try to find the field and extract value
        if f"{field_name}:" in cleaned_text:
            # Split on the field name with colon
            _, value = cleaned_text.split(f"{field_name}:", 1)
            return value.strip()
        
        # Try without colon
        if field_name in cleaned_text:
            _, value = cleaned_text.split(field_name, 1)
            # Clean up any remaining colons
            return value.lstrip(':').strip()
        
        # Special handling for dates in text
        if "scheduled for" in cleaned_text and any(d in field_name.lower() for d in ["date", "certification"]):
            match = re.search(r'scheduled for\s+(.+?)\.?\s*$', cleaned_text)
            if match:
                return match.group(1).strip()
            
        return None

    def extract_multiline_value(self, paragraphs: List[any], start_idx: int) -> tuple[str, int]:
        """Extract multiline value starting from given index."""
        content_lines = []
        i = start_idx + 1  # Start from next line
        
        while (i < len(paragraphs) and 
               paragraphs[i].text.strip() and 
               not any(field in paragraphs[i].text for field in self.field_mappings)):
            content_lines.append(paragraphs[i].text.strip())
            i += 1
            
        return '\n'.join(content_lines), i - 1  # Return content and last processed index

    def extract_conditional_block(self, paragraphs: List[any], start_idx: int) -> Optional[str]:
        """Extract selected option from conditional block."""
        i = start_idx
        while i < len(paragraphs):
            text = paragraphs[i].text.strip()
            for option, value in self.checkbox_mappings.items():
                if "☒" in text and option.replace("☒", "").strip() in text:
                    return value
            i += 1
        return None
    
    def extract_data(self, doc: Document) -> Dict[str, str]:
        """Extract all field values from the worksheet."""
        extracted_content = {placeholder: "" for _, placeholder in self.field_mappings.items()}
        
        paragraphs = list(doc.paragraphs)
        i = 0
        while i < len(paragraphs):
            current_text = paragraphs[i].text.strip()
            logger.debug(f"Processing text: {current_text}")
            
            # Handle Q6 conditional block
            if "6. Check the appropriate box and complete:" in current_text:
                if project_type := self.extract_conditional_block(paragraphs, i + 1):
                    extracted_content["{ProjectType}"] = project_type
                i += 1
                continue
            
            # Handle multiline fields
            multiline_matched = False
            for field in self.multiline_fields:
                if field in current_text:
                    value, last_idx = self.extract_multiline_value(paragraphs, i)
                    extracted_content[self.field_mappings[field]] = value
                    i = last_idx
                    multiline_matched = True
                    break
            
            if not multiline_matched:
                # Handle single-line fields with flexible matching
                current_normalized = re.sub(r'\s*:\s*', ':', current_text)
                for field, placeholder in self.field_mappings.items():
                    field_normalized = re.sub(r'\s*:\s*', ':', field)
                    # Try to match field name without being strict about colon placement
                    field_base = field_normalized.rstrip(':')
                    if field_base in current_normalized:
                        logger.debug(f"Found field match: {field_base} in {current_normalized}")
                        value = current_normalized.split(field_base, 1)[1].lstrip(':').strip()
                        if value:
                            extracted_content[placeholder] = value
                            logger.debug(f"Extracted value: {value} for {placeholder}")
                            break
            
            i += 1
        
        # Process tables
        for table in doc.tables:
            self.process_table(table, extracted_content)
        
        return extracted_content

    def process_table(self, table, extracted_content):
        """Process table to extract field values."""
        for row in table.rows:
            if len(row.cells) >= 2:
                cell_text = self.clean_text(row.cells[0].text)
                cell_value = self.clean_text(row.cells[1].text)
                
                # Try exact match first
                for field, placeholder in self.field_mappings.items():
                    if field == cell_text:
                        extracted_content[placeholder] = cell_value
                        logger.info(f"Found exact match {placeholder} in table: {cell_value}")
                        break
                
                # If no exact match, try contains match
                if not any(field == cell_text for field in self.field_mappings):
                    for field, placeholder in self.field_mappings.items():
                        if field in cell_text:
                            extracted_content[placeholder] = cell_value
                            logger.info(f"Found partial match {placeholder} in table: {cell_value}")
                            break
