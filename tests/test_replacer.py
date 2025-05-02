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

def test_split_placeholder():
    """Test replacing a placeholder split across multiple runs."""
    doc = Document()
    p = doc.add_paragraph()
    p.add_run("Contact: {")
    p.add_run("SME")
    p.add_run("Name}")
    
    replacer = PlaceholderReplacer()
    replacements = {"{SMEName}": "John Doe"}
    
    replacer.process_paragraph(p, replacements)
    assert "John Doe" in p.text
    assert "{SMEName}" not in p.text

def test_multiple_replacements_in_run():
    """Test multiple replacements in a single run."""
    doc = Document()
    p = doc.add_paragraph("Name: {SMEName}, Email: {SMEEmail}")
    
    replacer = PlaceholderReplacer()
    replacements = {
        "{SMEName}": "John Doe",
        "{SMEEmail}": "john@example.com"
    }
    
    replacer.process_paragraph(p, replacements)
    assert "John Doe" in p.text
    assert "john@example.com" in p.text
    assert "{SMEName}" not in p.text
    assert "{SMEEmail}" not in p.text

def test_preserve_formatting():
    """Test that formatting is preserved after replacement."""
    doc = Document()
    p = doc.add_paragraph()
    run = p.add_run("{SMEName}")
    run.bold = True
    run.italic = True
    
    replacer = PlaceholderReplacer()
    replacements = {"{SMEName}": "John Doe"}
    
    replacer.process_paragraph(p, replacements)
    assert "John Doe" in p.text
    assert p.runs[0].bold
    assert p.runs[0].italic

def test_empty_runs():
    """Test handling of empty runs in paragraph."""
    doc = Document()
    p = doc.add_paragraph()
    p.add_run("")  # Empty run
    p.add_run("{SMEName}")
    p.add_run("")  # Empty run
    
    replacer = PlaceholderReplacer()
    replacements = {"{SMEName}": "John Doe"}
    
    replacer.process_paragraph(p, replacements)
    assert "John Doe" in p.text

def test_partial_placeholder():
    """Test handling of partial/malformed placeholders."""
    doc = Document()
    p = doc.add_paragraph("Contact: {SMEName, Phone: SMEPhone}")  # Missing closing brace
    
    replacer = PlaceholderReplacer()
    replacements = {"{SMEName}": "John Doe"}
    
    replacer.process_paragraph(p, replacements)
    assert p.text == "Contact: {SMEName, Phone: SMEPhone}"  # Should not modify malformed placeholders
