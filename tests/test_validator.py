# pytest tests/test_validator.py -v

import pytest
import os
from faa_sc_filler.validator import DocumentValidator

def test_file_size_validation(tmp_path):
    # Create a large test file
    large_file = tmp_path / "large.docx"
    large_file.write_bytes(b'0' * (11 * 1024 * 1024))  # 11MB
    
    validator = DocumentValidator()
    with pytest.raises(ValueError, match="File too large"):
        validator.validate_docx(str(large_file))

def test_required_fields():
    validator = DocumentValidator()
    content = {
        "Applicant": "Test Corp",
        "Model": "Test-100"
        # Missing Summary
    }
    missing = validator.validate_required_fields(content)
    assert "Summary" in missing

def test_invalid_file_format(tmp_path):
    # Create a text file with .docx extension
    fake_docx = tmp_path / "fake.docx"
    fake_docx.write_text("This is not a real DOCX file")
    
    validator = DocumentValidator()
    with pytest.raises(ValueError, match="Not a valid DOCX file"):
        validator.validate_docx(str(fake_docx))

def test_missing_file():
    validator = DocumentValidator()
    with pytest.raises(FileNotFoundError):
        validator.validate_docx("nonexistent.docx")

def test_multiple_missing_fields():
    validator = DocumentValidator()
    content = {
        "Applicant": "Test Corp",
        # Missing Model, Summary, Description, SpecialConditions
    }
    missing = validator.validate_required_fields(content)
    assert "Model" in missing
    assert "Summary" in missing
    assert "Description" in missing
    assert "SpecialConditions" in missing
    assert len(missing) == 4  # Update expected count

def test_empty_field_values():
    validator = DocumentValidator()
    content = {
        "Applicant": "",
        "Model": "   ",  # Whitespace only
        "Summary": None,  # None value
        "Description": "\n\t ",  # Only whitespace chars
    }
    missing = set(validator.validate_required_fields(content))
    expected = {"Applicant", "Model", "Summary", "Description"}
    assert missing.issuperset(expected)

def test_valid_docx(tmp_path):
    # Create minimal valid DOCX structure
    docx_file = tmp_path / "valid.docx"
    with open(docx_file, "wb") as f:
        # Write ZIP local file header signature
        f.write(b"PK\x03\x04")
        # Write minimal [Content_Types].xml entry
        f.write(b"PK\x03\x04\x14\x00\x00\x00\x08\x00")
        f.write(b"[Content_Types].xml")
    
    validator = DocumentValidator()
    try:
        validator.validate_docx(str(docx_file))
    except ValueError as e:
        pytest.fail(f"Should accept minimal DOCX structure: {e}")
