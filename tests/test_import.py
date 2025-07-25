import typing
import pytest

if not typing.TYPE_CHECKING:
    pytest.importorskip("docx")


def test_package_importable() -> None:
    """The package should be importable."""
    import scdocbuilder

    assert hasattr(scdocbuilder, "fill_template")
