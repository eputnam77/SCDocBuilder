import typing
from typing import Any, Callable, TypeVar
from pathlib import Path
import pytest
from faa_sc_replacer.io import validate_input_files
from tests.property.strategies import docx_path

F = TypeVar("F", bound=Callable[..., Any])

if typing.TYPE_CHECKING:
    from hypothesis import given as given_decorator
    from hypothesis import settings, HealthCheck
else:
    hypothesis = pytest.importorskip("hypothesis")
    given_decorator: Callable[[F], F] = typing.cast(Callable[[F], F], hypothesis.given)
    settings = hypothesis.settings
    HealthCheck = hypothesis.HealthCheck


@pytest.mark.property
@settings(suppress_health_check=(HealthCheck.function_scoped_fixture,))
@typing.cast(Any, given_decorator)(template=docx_path(), worksheet=docx_path())  # type: ignore[misc]
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
