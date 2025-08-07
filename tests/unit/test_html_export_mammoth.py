from io import BytesIO
from types import SimpleNamespace
import sys

import pytest

if not pytest.__dict__.get("skip", False):
    pytest.importorskip("docx")

from docx import Document
from scdocbuilder.html_export import export_html


def test_export_html_uses_mammoth_and_bleach(monkeypatch):
    doc = Document()
    doc.add_paragraph("hello")

    calls = {"mammoth": False, "bleach": False}

    def fake_convert(fileobj, **_):
        assert isinstance(fileobj, BytesIO)
        calls["mammoth"] = True

        class Result:
            value = "<p>hi</p>"

        return Result()

    def fake_clean(html, tags=None, strip=False, **_):
        calls["bleach"] = html == "<p>hi</p>" and strip
        return html

    monkeypatch.setitem(
        sys.modules, "mammoth", SimpleNamespace(convert_to_html=fake_convert)
    )
    monkeypatch.setitem(sys.modules, "bleach", SimpleNamespace(clean=fake_clean))

    html = export_html(doc)
    assert html == "<p>hi</p>"
    assert calls["mammoth"] and calls["bleach"]
