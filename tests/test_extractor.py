# pytest tests/test_extractor.py -v

import pytest
from docx import Document
from faa_sc_filler.extractor import WorksheetExtractor

def test_extract_simple_field(sample_worksheet):
    extractor = WorksheetExtractor()
    data = extractor.extract_data(sample_worksheet)
    
    assert data["{ApplicantName}"] == "Test Corp"
    assert data["{AirplaneManufacturer}"] == "Boeing"
    assert data["{AirplaneModel}"] == "787-TEST"

def test_extract_multiline_field(multiline_worksheet):
    extractor = WorksheetExtractor()
    data = extractor.extract_data(multiline_worksheet)
    
    assert "{Description}" in data
    assert "Line 1" in data["{Description}"]
    assert "Line 2" in data["{Description}"]
    assert "Line 3" in data["{Description}"]

def test_extract_missing_field(sample_worksheet):
    extractor = WorksheetExtractor()
    data = extractor.extract_data(sample_worksheet)
    
    assert "{SMEName}" in data
    assert data["{SMEName}"] == ""  # Should return empty string for missing fields

def test_extract_table_data():
    doc = Document()
    table = doc.add_table(rows=2, cols=2)
    table.cell(0, 0).text = "Maximum passenger capacity of all listed aircraft:"
    table.cell(0, 1).text = "244"
    
    extractor = WorksheetExtractor()
    data = extractor.extract_data(doc)
    
    assert data["{PassengerCapacity}"] == "244"

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
