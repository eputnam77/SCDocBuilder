from json import loads
import logging
from pathlib import Path
from typing import Any
import pytest

from scdocbuilder.cli import main, ErrorCode


def test_logging_produces_json(tmp_path: Path, caplog: Any) -> None:
    template = tmp_path / "missing.docx"
    worksheet = tmp_path / "missing.docx"
    with pytest.raises(SystemExit):
        with caplog.at_level(logging.ERROR):
            main(["--template", str(template), "--worksheet", str(worksheet)])
    record = caplog.records[0]
    data = loads(record.message)
    assert {"event", "field", "old", "new"} <= data.keys()


def test_logging_records_worksheet_error(tmp_path: Path, caplog: Any) -> None:
    template = tmp_path / "missing.docx"
    worksheet = tmp_path / "missing.docx"
    with pytest.raises(SystemExit) as exc:
        with caplog.at_level(logging.ERROR):
            main(["--template", str(template), "--worksheet", str(worksheet)])
    assert exc.value.code == ErrorCode.ENOFILE
    assert any("worksheet_parse_error" in r.message for r in caplog.records)
