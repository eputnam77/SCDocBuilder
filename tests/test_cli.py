from datetime import datetime
from pathlib import Path
from typing import Any
import logging
from logging.handlers import RotatingFileHandler

import pytest

from faa_sc_replacer.cli import ErrorCode, main, parse_args
from docx import Document


def test_parse_args_parses_required() -> None:
    args = parse_args(
        [
            "--template",
            "t.docx",
            "--worksheet",
            "w.docx",
            "--dry-run",
            "--log-level",
            "DEBUG",
        ]
    )
    assert args.template == "t.docx"
    assert args.worksheet == "w.docx"
    assert args.dry_run is True
    assert args.log_level == "DEBUG"


def test_parse_args_parses_batch() -> None:
    args = parse_args(
        [
            "--template",
            "t.docx",
            "--batch",
            "worksheets",
        ]
    )

    assert args.template == "t.docx"
    assert args.batch == "worksheets"
    assert args.worksheet is None


def test_main_prints_output_path(tmp_path: Path, capsys: Any, monkeypatch: Any) -> None:
    """CLI should print the absolute output path when no --output is given."""

    template = tmp_path / "t.docx"
    worksheet = tmp_path / "w.docx"
    Document().save(str(template))
    ws_doc = Document()
    ws_doc.add_paragraph("Applicant name: Foo")
    ws_doc.save(str(worksheet))

    fixed_time = datetime(2024, 1, 2, 3, 4, 5)

    class FixedDateTime(datetime):
        @classmethod
        def now(cls) -> datetime:  # type: ignore[override]
            return fixed_time

    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr("faa_sc_replacer.cli.datetime", FixedDateTime)

    main(
        [
            "--template",
            str(template),
            "--worksheet",
            str(worksheet),
        ]
    )

    expected = tmp_path / f"t_{fixed_time:%Y%m%d_%H%M%S}.docx"
    assert expected.exists()
    captured = capsys.readouterr()
    assert captured.out.strip() == str(expected.resolve())


def test_main_missing_file_exits_with_code(tmp_path: Path) -> None:
    """CLI should exit with ENOFILE when files are missing."""

    missing = tmp_path / "missing.docx"
    with pytest.raises(SystemExit) as exc:
        main(
            [
                "--template",
                str(missing),
                "--worksheet",
                str(missing),
            ]
        )

    assert exc.value.code == ErrorCode.ENOFILE


def test_main_batch_processes_directory(tmp_path: Path, monkeypatch: Any) -> None:
    template = tmp_path / "t.docx"
    Document().save(str(template))
    batch_dir = tmp_path / "ws"
    batch_dir.mkdir()
    for i in range(2):
        doc = Document()
        doc.add_paragraph("Applicant name: Foo")
        doc.save(str(batch_dir / f"w{i}.docx"))

    fixed_time = datetime(2024, 1, 1, 1, 1, 1)

    class FixedDateTime(datetime):
        @classmethod
        def now(cls) -> datetime:  # type: ignore[override]
            return fixed_time

    monkeypatch.setattr("faa_sc_replacer.cli.datetime", FixedDateTime)
    monkeypatch.chdir(tmp_path)

    main(
        [
            "--template",
            str(template),
            "--batch",
            str(batch_dir),
        ]
    )

    for i in range(2):
        expected = batch_dir / f"w{i}_{fixed_time:%Y%m%d_%H%M%S}.docx"
        assert expected.exists()


def test_logging_rotation_configured(tmp_path: Path, monkeypatch: Any) -> None:
    template = tmp_path / "t.docx"
    worksheet = tmp_path / "w.docx"
    Document().save(str(template))
    ws_doc = Document()
    ws_doc.add_paragraph("Applicant name: Foo")
    ws_doc.save(str(worksheet))

    monkeypatch.chdir(tmp_path)
    logging.getLogger().handlers.clear()
    main(
        [
            "--template",
            str(template),
            "--worksheet",
            str(worksheet),
        ]
    )

    handlers = logging.getLogger().handlers
    assert any(
        isinstance(h, RotatingFileHandler) and h.maxBytes == 5 * 1024 * 1024
        for h in handlers
    )
    logging.getLogger().handlers.clear()
