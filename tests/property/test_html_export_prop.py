from typing import Any, Callable, TypeVar, cast
import typing

import pytest
from docx import Document
from faa_sc_replacer.html_export import export_html

F = TypeVar("F", bound=Callable[..., Any])

if typing.TYPE_CHECKING:
    from hypothesis import given as given_decorator
    from hypothesis import strategies as st
    from hypothesis import settings, HealthCheck

    property_mark: Callable[[F], F]
else:
    hypothesis = pytest.importorskip("hypothesis")
    given_decorator = cast(Callable[[F], F], hypothesis.given)
    st = hypothesis.strategies
    settings = hypothesis.settings
    HealthCheck = hypothesis.HealthCheck
    property_mark = cast(Callable[[F], F], pytest.mark.property)


@property_mark
@settings(suppress_health_check=(HealthCheck.function_scoped_fixture,))
@given_decorator(text=st.text())
def test_export_html_returns_string(text: str) -> None:
    doc = Document()
    doc.add_paragraph(text)
    html = export_html(doc)
    assert isinstance(html, str)
