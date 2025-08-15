import typing
from typing import Any, Mapping
import pytest
import builtins
import importlib

if typing.TYPE_CHECKING:
    from docx import Document
else:
    pytest.importorskip("docx")
    from docx import Document

from scdocbuilder.html_export import export_html

LIBS_AVAILABLE = (
    importlib.util.find_spec("mammoth") is not None
    and importlib.util.find_spec("bleach") is not None
)


def test_export_html_returns_string() -> None:
    doc = Document()
    doc.add_paragraph("Hello")

    html = export_html(doc)

    assert "<p" in html


def test_export_html_strips_script_tags() -> None:
    doc = Document()
    doc.add_paragraph("<script>alert('x')</script>")
    html = export_html(doc)
    assert "<script" not in html


def test_export_html_produces_heading_tags_fallback(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    original_import = builtins.__import__

    def fake_import(
        name: str,
        globals: Mapping[str, Any] | None = None,
        locals: Mapping[str, Any] | None = None,
        fromlist: tuple[str, ...] = (),
        level: int = 0,
    ) -> Any:
        if name in {"mammoth", "bleach"}:
            raise ImportError
        return original_import(name, globals, locals, fromlist, level)

    monkeypatch.setattr(builtins, "__import__", fake_import)

    doc = Document()
    doc.add_heading("Title", level=5)
    html = export_html(doc)
    assert "<h5>Title</h5>" in html


@pytest.mark.skipif(not LIBS_AVAILABLE, reason="mammoth/bleach not installed")
def test_export_html_produces_heading_tags_with_libs() -> None:
    doc = Document()
    doc.add_heading("Title", level=5)
    html = export_html(doc)
    assert "<h5>Title</h5>" in html
