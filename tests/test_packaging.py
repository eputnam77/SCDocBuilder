from pathlib import Path
import tomllib


def test_console_script_entrypoint() -> None:
    """pyproject.toml should expose `scdocbuilder` console script."""
    data = tomllib.loads(Path("pyproject.toml").read_text())
    scripts = data.get("tool", {}).get("poetry", {}).get("scripts", {})
    assert scripts.get("scdocbuilder") == "scdocbuilder.cli:main"
