# pytest tests/test_cli.py -v

import os
import sys

import pytest
from docx import Document

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
)

from faa_sc_filler.cli import main, parse_args
from faa_sc_filler.config import DEFAULT_CONFIG
from faa_sc_filler.prompt import prompt_for_missing_fields
from faa_sc_filler.validator import DocumentValidator


@pytest.fixture
def sample_files(tmp_path):
    """Create sample input files for testing."""
    template_path = tmp_path / "template.docx"
    worksheet_path = tmp_path / "worksheet.docx"
    output_path = tmp_path / "output.docx"

    # Create test template
    template = Document()
    template.add_paragraph("Contact: {SMEName}")
    template.save(template_path)

    # Create test worksheet
    worksheet = Document()
    worksheet.add_paragraph("Name of SME: John Doe")
    worksheet.save(worksheet_path)

    return template_path, worksheet_path, output_path


# CLI Arguments Tests
def test_cli_required_args():
    with pytest.raises(SystemExit):
        parse_args([])  # No args


def test_cli_valid_args():
    args = parse_args(
        ["--template", "template.docx", "--worksheet", "worksheet.docx", "--dry-run"]
    )
    assert args.template == "template.docx"
    assert args.worksheet == "worksheet.docx"
    assert args.dry_run is True


def test_log_level_validation():
    args = parse_args(
        [
            "--template",
            "template.docx",
            "--worksheet",
            "worksheet.docx",
            "--log-level",
            "DEBUG",
        ]
    )
    assert args.log_level == "DEBUG"


def test_custom_need_token():
    custom_token = "[[MISSING:"
    args = parse_args(
        [
            "--template",
            "template.docx",
            "--worksheet",
            "worksheet.docx",
            "--need-token",
            custom_token,
        ]
    )
    assert args.need_token == custom_token


def test_output_path():
    output_path = "output/result.docx"
    args = parse_args(
        [
            "--template",
            "template.docx",
            "--worksheet",
            "worksheet.docx",
            "--output",
            output_path,
        ]
    )
    assert args.output == output_path


def test_invalid_log_level():
    with pytest.raises(SystemExit):
        parse_args(
            [
                "--template",
                "template.docx",
                "--worksheet",
                "worksheet.docx",
                "--log-level",
                "INVALID",
            ]
        )


def test_default_values():
    args = parse_args(["--template", "template.docx", "--worksheet", "worksheet.docx"])
    assert args.need_token == DEFAULT_CONFIG["need_token"]
    assert args.log_level == "INFO"
    assert args.dry_run is False
    assert args.output is None


def test_nonexistent_files():
    args = parse_args(["--template", "nonexistent.docx", "--worksheet", "missing.docx"])
    assert args.template == "nonexistent.docx"
    assert args.worksheet == "missing.docx"


def test_combined_arguments():
    args = parse_args(
        [
            "--template",
            "template.docx",
            "--worksheet",
            "worksheet.docx",
            "--output",
            "output.docx",
            "--dry-run",
            "--log-level",
            "DEBUG",
            "--need-token",
            "[[MISSING:",
        ]
    )
    assert args.template == "template.docx"
    assert args.worksheet == "worksheet.docx"
    assert args.output == "output.docx"
    assert args.dry_run is True
    assert args.log_level == "DEBUG"
    assert args.need_token == "[[MISSING:"


def test_help_text():
    with pytest.raises(SystemExit) as exc_info:
        parse_args(["--help"])
    assert exc_info.value.code == 0


def test_version():
    with pytest.raises(SystemExit) as exc_info:
        parse_args(["--version"])
    assert exc_info.value.code == 0  # Version info exits cleanly


# Document Validation Tests
def test_cfr_part_validation():
    """Test CFR part validation."""
    assert DocumentValidator.validate_cfr_part("25") is True
    assert DocumentValidator.validate_cfr_part("25,27") is True
    assert DocumentValidator.validate_cfr_part("25, 27") is True
    assert DocumentValidator.validate_cfr_part("24") is False
    assert DocumentValidator.validate_cfr_part("25,24") is False


def test_docket_notice_validation():
    """Test docket and notice number validation."""
    validator = DocumentValidator()
    assert validator.validate_docket_no("FAA-2024-0001") is True
    assert validator.validate_docket_no("FAA-24-1") is False

    assert validator.validate_notice_no("24-01-01-SC") is True
    assert validator.validate_notice_no("24-1-1-SC") is False


# Field Prompt Tests
@pytest.mark.parametrize(
    "inputs,expected",
    [
        (["25", "FAA-2024-0001", "24-01-01-SC"], True),
        (["invalid", "FAA-2024-0001", "24-01-01-SC"], False),
    ],
)
def test_prompt_for_missing_fields(monkeypatch, inputs, expected):
    """Test prompting for missing fields."""
    responses = iter(inputs)
    monkeypatch.setattr("builtins.input", lambda _: next(responses))

    data = {}
    if expected:
        result = prompt_for_missing_fields(data)
        assert all(k in result for k in ["{CFRPart}", "{DocketNo}", "{NoticeNo}"])
    else:
        with pytest.raises(ValueError):  # Expect ValueError for invalid input
            prompt_for_missing_fields(data)


# Integration Tests
def test_cli_end_to_end(sample_files, monkeypatch, caplog):
    """Test complete CLI workflow."""
    template_path, worksheet_path, output_path = sample_files

    # Mock user inputs
    inputs = iter(
        [
            "25",  # CFR Part
            "FAA-2024-0001",  # Docket No
            "24-01-01-SC",  # Notice No
        ]
    )
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    # Run CLI with args
    main_result = main(
        [
            "--template",
            str(template_path),
            "--worksheet",
            str(worksheet_path),
            "--output",
            str(output_path),
            "--log-level",
            "DEBUG",  # Add debug logging
        ]
    )

    # Print logs for debugging
    print("\nLog output:")
    for record in caplog.records:
        print(f"{record.levelname}: {record.message}")

    # Verify results
    assert (
        main_result == 0
    ), f"Main returned {main_result}. Check logs above for details."
    assert output_path.exists(), f"Output file not created at {output_path}"

    # Check content was properly replaced
    output_doc = Document(output_path)
    assert (
        "Contact: John Doe" in output_doc.paragraphs[0].text
    ), "Expected text not found in output"
    assert (
        "[[NEED:" not in output_doc.paragraphs[0].text
    ), "Unfilled token found in output"
