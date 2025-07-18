from __future__ import annotations

from pathlib import Path
import typing
import pytest

if typing.TYPE_CHECKING:
    from hypothesis import strategies as st
else:
    hypothesis = pytest.importorskip("hypothesis")
    st = hypothesis.strategies


def docx_path() -> st.SearchStrategy[Path]:
    """Generate fake .docx file paths."""
    return st.text(
        min_size=1,
        max_size=10,
        alphabet=st.characters(min_codepoint=97, max_codepoint=122),
    ).map(lambda name: Path(f"{name}.docx"))


def log_level() -> st.SearchStrategy[str]:
    """Generate valid logging levels."""
    return st.sampled_from(["DEBUG", "INFO", "WARNING", "ERROR"])


def placeholder_dict() -> st.SearchStrategy[dict[str, str]]:
    """Generate small dictionaries of placeholder replacements."""
    keys = st.text(min_size=1, max_size=20)
    values = st.text(min_size=0, max_size=50)
    return st.dictionaries(keys, values, max_size=5)
