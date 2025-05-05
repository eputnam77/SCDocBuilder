import pytest
from docx import Document
from faa_sc_filler.extractor import WorksheetExtractor

# Basic field extraction tests
def test_extract_simple_field(sample_worksheet):
    extractor = WorksheetExtractor()
    data = extractor.extract_data(sample_worksheet)
    
    assert data["{ApplicantName}"] == "Test Corp"
    assert data["{AirplaneManufacturer}"] == "Boeing"
    assert data["{AirplaneModel}"] == "787-TEST"

def test_extract_multiline_field(multiline_worksheet):
    """Test extraction of multiline content."""
    extractor = WorksheetExtractor()
    data = extractor.extract_data(multiline_worksheet)
    
    print(f"Extracted data: {data}")  # Debug print
    assert "{Description}" in data  # Fix the assertion key
    assert data["{Description}"] == "Line 1\nLine 2\nLine 3"

def test_extract_missing_field(sample_worksheet):
    extractor = WorksheetExtractor()
    data = extractor.extract_data(sample_worksheet)
    
    assert "{SMEName}" in data
    assert data["{SMEName}"] == ""  # Should return empty string for missing fields

def test_extract_numbered_field():
    doc = Document()
    doc.add_paragraph("a. Type of airplane: transport category, freighter, VIP, business jet, etc.: Transport Category")
    
    extractor = WorksheetExtractor()
    data = extractor.extract_data(doc)
    
    assert data["{AirplaneType}"] == "Transport Category"

def test_extract_multiline_summary():
    doc = Document()
    doc.add_paragraph("Briefly (one to three sentences) provide a summary of the novel or unusual design features of the airplane.")
    doc.add_paragraph("First feature description")
    doc.add_paragraph("Second feature description")
    
    extractor = WorksheetExtractor()
    data = extractor.extract_data(doc)
    
    assert "{Summary}" in data
    assert "First feature" in data["{Summary}"]
    assert "Second feature" in data["{Summary}"]

def test_empty_field_handling():
    doc = Document()
    doc.add_paragraph("Applicant name:")  # No value after colon
    
    extractor = WorksheetExtractor()
    data = extractor.extract_data(doc)
    
    assert data["{ApplicantName}"] == ""

def test_malformed_field_label():
    doc = Document()
    doc.add_paragraph("Applicant name :Test Corp")  # Extra space before colon
    
    extractor = WorksheetExtractor()
    data = extractor.extract_data(doc)
    
    assert data["{ApplicantName}"] == "Test Corp"

def test_conditional_q6_block():
    doc = Document()
    doc.add_paragraph("6. Check the appropriate box and complete:")
    doc.add_paragraph("☒ This is a new TC project")
    doc.add_paragraph("☐ This is an amended TC project")
    
    extractor = WorksheetExtractor()
    data = extractor.extract_data(doc)
    
    assert data["{ProjectType}"] == "new TC"

def test_multiple_whitespace_handling():
    doc = Document()
    doc.add_paragraph("CPN project number:    12345    ")
    
    extractor = WorksheetExtractor()
    data = extractor.extract_data(doc)
    
    assert data["{CPN}"] == "12345"

def test_date_field_extraction():
    doc = Document()
    doc.add_paragraph("Date of application: 2025-04-21")
    
    extractor = WorksheetExtractor()
    data = extractor.extract_data(doc)
    
    assert data["{ApplicationDate}"] == "2025-04-21"

def test_mixed_formatting():
    doc = Document()
    p = doc.add_paragraph()
    run1 = p.add_run("Applicant name: ")
    run1.bold = True
    run2 = p.add_run("Test Corp")
    run2.italic = True
    
    extractor = WorksheetExtractor()
    data = extractor.extract_data(doc)
    assert data["{ApplicantName}"] == "Test Corp"

def test_special_characters():
    doc = Document()
    doc.add_paragraph("SME Regional Office address: 123 Main St., Suite #4, Bldg. A & B")
    
    extractor = WorksheetExtractor()
    data = extractor.extract_data(doc)
    assert data["{SMEROAddress}"] == "123 Main St., Suite #4, Bldg. A & B"

def test_multiple_colons():
    doc = Document()
    doc.add_paragraph("Type of airplane: transport category, freighter, VIP, business jet, etc.: Transport Category")
    
    extractor = WorksheetExtractor()
    data = extractor.extract_data(doc)
    assert data["{AirplaneType}"] == "Transport Category"

def test_false_placeholder_text():
    doc = Document()
    doc.add_paragraph("Text with {braces} but not a placeholder")
    doc.add_paragraph("Applicant name: Test Corp")
    
    extractor = WorksheetExtractor()
    data = extractor.extract_data(doc)
    assert data["{ApplicantName}"] == "Test Corp"
    assert "{braces}" not in data.values()

def test_certification_date_field():
    doc = Document()
    doc.add_paragraph("Anticipated certification date: 2025-06-30")
    
    extractor = WorksheetExtractor()
    data = extractor.extract_data(doc)
    
    assert "{CertDate}" in data
    assert data["{CertDate}"] == "2025-06-30"

def test_cfr_part_extraction():
    """Test CFR part extraction."""
    doc = Document()
    doc.add_paragraph("14 CFR Part 25")
    
    extractor = WorksheetExtractor()
    data = extractor.extract_data(doc)
    
    print(f"Raw paragraph text: {doc.paragraphs[0].text}")  # Debug print
    print(f"Extracted data: {data}")  # Debug print
    assert data["{CFRPart}"] == "25"

def test_modifier_name_extraction():
    doc = Document()
    doc.add_paragraph("Name of Modifier: Test Modifier Inc.")
    
    extractor = WorksheetExtractor()
    data = extractor.extract_data(doc)
    
    assert "{Modifier}" in data
    assert data["{Modifier}"] == "Test Modifier Inc."
