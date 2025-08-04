import pytest
import typing
from pathlib import Path

if typing.TYPE_CHECKING:
    from docx import Document
else:
    pytest.importorskip("docx")
    from docx import Document

try:
    from fastapi.testclient import TestClient
except Exception:  # pragma: no cover - optional dependency
    pytest.skip("fastapi not installed", allow_module_level=True)

from scdocbuilder.api import app


def _make_docs(tmp_path: Path) -> tuple[Path, Path]:
    template = tmp_path / "t.docx"
    tdoc = Document()
    tdoc.add_paragraph("{Applicant name} {Airplane model}")
    tdoc.save(str(template))

    worksheet = tmp_path / "w.docx"
    wdoc = Document()
    wdoc.add_paragraph("Applicant name: Foo")
    wdoc.add_paragraph("Airplane model: Bar")
    wdoc.add_paragraph("Question 15:")
    wdoc.add_paragraph("Ans15")
    wdoc.add_paragraph("Question 16:")
    wdoc.add_paragraph("Ans16")
    wdoc.add_paragraph("Question 17:")
    wdoc.add_paragraph("Ans17")
    wdoc.save(str(worksheet))
    return template, worksheet


def test_generate_endpoint_returns_doc(tmp_path: Path) -> None:
    template, worksheet = _make_docs(tmp_path)
    client = TestClient(app)
    with template.open("rb") as t, worksheet.open("rb") as w:
        resp = client.post(
            "/generate",
            files={
                "template": (
                    "t.docx",
                    t,
                    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                ),
                "worksheet": (
                    "w.docx",
                    w,
                    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                ),
            },
        )
    assert resp.status_code == 200
    assert resp.content.startswith(b"PK")


def test_generate_endpoint_returns_html(tmp_path: Path) -> None:
    template, worksheet = _make_docs(tmp_path)
    client = TestClient(app)
    with template.open("rb") as t, worksheet.open("rb") as w:
        resp = client.post(
            "/generate?html=true",
            files={
                "template": (
                    "t.docx",
                    t,
                    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                ),
                "worksheet": (
                    "w.docx",
                    w,
                    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                ),
            },
        )
    assert resp.status_code == 200
    assert "<p" in resp.text


def test_health_endpoint_returns_ok() -> None:
    client = TestClient(app)
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}
