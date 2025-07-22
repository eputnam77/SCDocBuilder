from typing import Any, Callable, TypeVar, cast
import typing
from pathlib import Path

import pytest
from tests.property.strategies import docx_path
from faa_sc_replacer.benchmark import benchmark_processing

if typing.TYPE_CHECKING:
    from docx import Document
else:
    pytest.importorskip("docx")
    from docx import Document

F = TypeVar("F", bound=Callable[..., Any])

if typing.TYPE_CHECKING:
    from hypothesis import given as given_decorator
    from hypothesis import settings, HealthCheck

    property_mark: Callable[[F], F]
else:
    hypothesis = pytest.importorskip("hypothesis")
    given_decorator = cast(Callable[[F], F], hypothesis.given)
    settings = hypothesis.settings
    HealthCheck = hypothesis.HealthCheck
    property_mark = cast(Callable[[F], F], pytest.mark.property)


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
