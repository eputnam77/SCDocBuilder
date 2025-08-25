from typing import Any, Callable, TYPE_CHECKING, cast, no_type_check
from pathlib import Path
import pytest

if not TYPE_CHECKING:
    pytest.importorskip("docx")

from io import BytesIO

from docx import Document
from scdocbuilder.io import validate_input_files
from tests.property.strategies import docx_path

Decorator = Callable[[Callable[..., Any]], Callable[..., Any]]

if TYPE_CHECKING:
    from hypothesis import HealthCheck, given as given_decorator, settings

    def property_mark(func: Callable[..., Any]) -> Callable[..., Any]: ...

else:
    hypothesis = pytest.importorskip("hypothesis")
    given_decorator = cast(Decorator, hypothesis.given)
    settings = hypothesis.settings
    HealthCheck = hypothesis.HealthCheck
    property_mark = cast(Decorator, pytest.mark.property)


# Pre-generate minimal DOCX bytes once to avoid per-example Document writes,
# which were slow enough to trip Hypothesis' default deadline. Writing bytes is
# much faster and still exercises `validate_input_files` with real DOCX data.
_buf = BytesIO()
Document().save(_buf)
DOCX_BYTES = _buf.getvalue()


@no_type_check
@property_mark
@settings(deadline=None, suppress_health_check=(HealthCheck.function_scoped_fixture,))
@given_decorator(template=docx_path(), worksheet=docx_path())
def test_validate_input_files_accepts_paths(
    tmp_path: Path, template: Path, worksheet: Path
) -> None:
    """validate_input_files should accept existing DOCX files."""

    t = tmp_path / template.name
    w = tmp_path / worksheet.name
    t.write_bytes(DOCX_BYTES)
    w.write_bytes(DOCX_BYTES)

    validate_input_files(t, w)

    with pytest.raises(FileNotFoundError):
        validate_input_files(t, tmp_path / "missing.docx")
