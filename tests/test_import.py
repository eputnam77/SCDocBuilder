def test_package_importable() -> None:
    """The package should be importable."""
    import faa_sc_replacer

    assert hasattr(faa_sc_replacer, "fill_template")
