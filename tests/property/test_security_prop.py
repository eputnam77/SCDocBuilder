from typing import Any, Callable, TypeVar, cast
import typing
from pathlib import Path

import pytest
from tests.property.strategies import docx_path
from faa_sc_replacer.security import reject_macros, cleanup_uploads

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
@given_decorator(
    name=st.text(
        min_size=1,
        max_size=10,
        alphabet=st.characters(min_codepoint=97, max_codepoint=122),
    )
)
def test_reject_macros_raises(name: str, tmp_path: Path) -> None:
    path = tmp_path / f"{name}.docm"
    path.write_bytes(b"dummy")
    with pytest.raises(ValueError):
        reject_macros(path)


@property_mark
@settings(suppress_health_check=(HealthCheck.function_scoped_fixture,))
@given_decorator(file=docx_path())
def test_cleanup_uploads_removes_files(tmp_path: Path, file: Path) -> None:
    p = tmp_path / file.name
    p.write_bytes(b"data")
    cleanup_uploads(p)
    assert not p.exists()
