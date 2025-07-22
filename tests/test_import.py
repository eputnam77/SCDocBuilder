import typing
import pytest

if not typing.TYPE_CHECKING:
    pytest.importorskip("docx")


def test_package_importable() -> None:
    """The package should be importable."""
    import faa_sc_replacer

    assert hasattr(faa_sc_replacer, "fill_template")
