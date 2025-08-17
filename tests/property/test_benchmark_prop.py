from typing import Any, Callable, TYPE_CHECKING, cast, no_type_check
from pathlib import Path

import pytest
from tests.property.strategies import docx_path
from scdocbuilder.benchmark import benchmark_processing

Decorator = Callable[[Callable[..., Any]], Callable[..., Any]]

if TYPE_CHECKING:
    from docx import Document
    from hypothesis import HealthCheck, given as given_decorator, settings

    def property_mark(func: Callable[..., Any]) -> Callable[..., Any]: ...
else:
    pytest.importorskip("docx")
    from docx import Document

    hypothesis = pytest.importorskip("hypothesis")
    given_decorator = cast(Decorator, hypothesis.given)
    settings = hypothesis.settings
    HealthCheck = hypothesis.HealthCheck
    property_mark = cast(Decorator, pytest.mark.property)


@no_type_check
@property_mark
@settings(
    suppress_health_check=(HealthCheck.function_scoped_fixture,),
    deadline=None,
)
@given_decorator(template=docx_path(), worksheet=docx_path())
def test_benchmark_returns_float(
    tmp_path: Path, template: Path, worksheet: Path
) -> None:
    t = tmp_path / template.name
    w = tmp_path / worksheet.name
    Document().save(str(t))
    Document().save(str(w))
    duration = benchmark_processing(t, w)
    assert isinstance(duration, float)
