from datetime import datetime
from pathlib import Path
from typing import Any

from faa_sc_replacer.cli import main, parse_args
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
