import typing
from typing import Any, Callable, TypeVar, cast, no_type_check
from pathlib import Path
import pytest

if not typing.TYPE_CHECKING:
    pytest.importorskip("docx")

from scdocbuilder.io import validate_input_files
from tests.property.strategies import docx_path

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


@no_type_check
@property_mark
@settings(suppress_health_check=(HealthCheck.function_scoped_fixture,))
@given_decorator(template=docx_path(), worksheet=docx_path())
def test_validate_input_files_accepts_paths(
    tmp_path: Path, template: Path, worksheet: Path
) -> None:
    """validate_input_files should accept existing DOCX files."""

    t = tmp_path / template.name
    w = tmp_path / worksheet.name
    t.write_bytes(b"\0")
    w.write_bytes(b"\0")

    validate_input_files(t, w)

    with pytest.raises(FileNotFoundError):
        validate_input_files(t, tmp_path / "missing.docx")
