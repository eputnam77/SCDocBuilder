# poetry run pytest

"""Test configuration and fixtures."""

import pytest
from docx import Document

try:
    import pytest_asyncio
    pytest_plugins = ["pytest_asyncio"]
except ImportError:
    pass  # asyncio support is optional

def pytest_configure(config):
    config.addinivalue_line(
        "markers", "asyncio: mark test as async/await test"
    )

@pytest.fixture
def sample_worksheet():
    doc = Document()
    # Add test data that matches real worksheet format
    doc.add_paragraph("Applicant name: Test Corp")
    doc.add_paragraph("Airplane manufacturer: Boeing")
    doc.add_paragraph("Airplane model: 787-TEST")
    return doc

@pytest.fixture
def multiline_worksheet():
    doc = Document()
    doc.add_paragraph("Provide a detailed discussion of the special conditions.")
    doc.add_paragraph("Line 1 of the response")
    doc.add_paragraph("Line 2 of the response")
    doc.add_paragraph("Line 3 of the response")
    return doc
