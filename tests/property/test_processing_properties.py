import pytest
from hypothesis import given
from hypothesis import strategies as st

from typing import Any

from faa_sc_replacer.processing import (
    extract_fields,
    replace_placeholders,
    apply_conditionals,
)
from tests.property.strategies import placeholder_dict


@pytest.mark.property
@given(doc=st.just(object()))
def test_extract_fields_not_implemented(doc: Any) -> None:
    """extract_fields is not yet implemented."""
    with pytest.raises(NotImplementedError):
        extract_fields(doc)


@pytest.mark.property
@given(doc=st.just(object()), values=placeholder_dict())
def test_replace_placeholders_not_implemented(doc: Any, values: dict[str, str]) -> None:
    """replace_placeholders is not yet implemented."""
    with pytest.raises(NotImplementedError):
        replace_placeholders(doc, values)


@pytest.mark.property
@given(doc=st.just(object()), values=placeholder_dict())
def test_apply_conditionals_not_implemented(doc: Any, values: dict[str, str]) -> None:
    """apply_conditionals is not yet implemented."""
    with pytest.raises(NotImplementedError):
        apply_conditionals(doc, values)
