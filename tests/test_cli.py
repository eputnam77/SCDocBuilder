# pytest tests/test_cli.py -v

import pytest
from faa_sc_filler.cli import parse_args
from faa_sc_filler.config import DEFAULT_CONFIG

def test_cli_required_args():
    with pytest.raises(SystemExit):
        parse_args([])  # No args

def test_cli_valid_args():
    args = parse_args([
        "--template", "template.docx",
        "--worksheet", "worksheet.docx",
        "--dry-run"
    ])
    assert args.template == "template.docx"
    assert args.worksheet == "worksheet.docx"
    assert args.dry_run is True

def test_log_level_validation():
    args = parse_args([
        "--template", "template.docx",
        "--worksheet", "worksheet.docx",
        "--log-level", "DEBUG"
    ])
    assert args.log_level == "DEBUG"

def test_custom_need_token():
    custom_token = "[[MISSING:"
    args = parse_args([
        "--template", "template.docx",
        "--worksheet", "worksheet.docx",
        "--need-token", custom_token
    ])
    assert args.need_token == custom_token

def test_output_path():
    output_path = "output/result.docx"
    args = parse_args([
        "--template", "template.docx",
        "--worksheet", "worksheet.docx",
        "--output", output_path
    ])
    assert args.output == output_path

def test_invalid_log_level():
    with pytest.raises(SystemExit):
        parse_args([
            "--template", "template.docx",
            "--worksheet", "worksheet.docx",
            "--log-level", "INVALID"
        ])

def test_default_values():
    args = parse_args([
        "--template", "template.docx",
        "--worksheet", "worksheet.docx"
    ])
    assert args.need_token == DEFAULT_CONFIG["need_token"]
    assert args.log_level == "INFO"
    assert args.dry_run is False
    assert args.output is None

def test_nonexistent_files():
    args = parse_args([
        "--template", "nonexistent.docx",
        "--worksheet", "missing.docx"
    ])
    assert args.template == "nonexistent.docx"
    assert args.worksheet == "missing.docx"

def test_combined_arguments():
    args = parse_args([
        "--template", "template.docx",
        "--worksheet", "worksheet.docx",
        "--output", "output.docx",
        "--dry-run",
        "--log-level", "DEBUG",
        "--need-token", "[[MISSING:"
    ])
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
