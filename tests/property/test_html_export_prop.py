from typing import Any, Callable, TypeVar, cast, no_type_check
import typing

import pytest

if typing.TYPE_CHECKING:
    from docx import Document
else:
    pytest.importorskip("docx")
    from docx import Document

from scdocbuilder.html_export import export_html

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


@no_type_check
@property_mark
@settings(suppress_health_check=(HealthCheck.function_scoped_fixture,))
@given_decorator(
    text=st.text(alphabet=st.characters(min_codepoint=32, max_codepoint=126))
)
def test_export_html_returns_string(text: str) -> None:
    doc = Document()
    doc.add_paragraph(text)
    html = export_html(doc)
    assert isinstance(html, str)
