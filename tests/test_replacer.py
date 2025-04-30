# pytest tests/test_replacer.py -v

import pytest
from docx import Document
from faa_sc_filler.replacer import PlaceholderReplacer

def test_placeholder_replacement():
    # Create test document with known placeholder
    doc = Document()
    doc.add_paragraph("Test SME Name: {SMEName}")
    
    replacer = PlaceholderReplacer()
    replacements = {"{SMEName}": "John Doe"}
    
    # Process the paragraph
    replacer.process_paragraph(doc.paragraphs[0], replacements)
    
    # Verify replacement
    assert "John Doe" in doc.paragraphs[0].text
    assert "{SMEName}" not in doc.paragraphs[0].text
