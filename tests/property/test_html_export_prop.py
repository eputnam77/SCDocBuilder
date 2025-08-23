from typing import Any, Callable, TYPE_CHECKING, cast, no_type_check

import pytest

if TYPE_CHECKING:
    from docx import Document
else:
    pytest.importorskip("docx")
    from docx import Document

from scdocbuilder.html_export import export_html

Decorator = Callable[[Callable[..., Any]], Callable[..., Any]]

if TYPE_CHECKING:
    from hypothesis import HealthCheck, given as given_decorator, settings
    from hypothesis import strategies as st

    def property_mark(func: Callable[..., Any]) -> Callable[..., Any]: ...

else:
    hypothesis = pytest.importorskip("hypothesis")
    given_decorator = cast(Decorator, hypothesis.given)
    st = hypothesis.strategies
    settings = hypothesis.settings
    HealthCheck = hypothesis.HealthCheck
    property_mark = cast(Decorator, pytest.mark.property)


@no_type_check
@property_mark
@settings(suppress_health_check=(HealthCheck.function_scoped_fixture,), deadline=None)
@given_decorator(
    text=st.text(alphabet=st.characters(min_codepoint=32, max_codepoint=126))
)
def test_export_html_returns_string(text: str) -> None:
    doc = Document()
    doc.add_paragraph(text)
    html = export_html(doc)
    assert isinstance(html, str)
