from pathlib import Path
import shutil
import subprocess

import pytest
import tomllib


def test_console_script_entrypoint() -> None:
    """pyproject.toml should expose `scdocbuilder` console script."""
    data = tomllib.loads(Path("pyproject.toml").read_text())
    scripts = data.get("tool", {}).get("poetry", {}).get("scripts", {})
    assert scripts.get("scdocbuilder") == "scdocbuilder.cli:main"


@pytest.mark.skipif(shutil.which("docker") is None, reason="Docker not installed")
def test_docker_image_help() -> None:
    """`docker run scdocbuilder --help` should print usage information."""
    build = subprocess.run(
        ["docker", "build", "-t", "scdocbuilder", "."],
        capture_output=True,
        text=True,
    )
    assert build.returncode == 0, build.stderr

    result = subprocess.run(
        ["docker", "run", "--rm", "scdocbuilder", "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "usage" in result.stdout.lower()


@pytest.mark.skipif(shutil.which("helm") is None, reason="Helm not installed")
@pytest.mark.xfail(reason="Helm chart not yet provided")
def test_helm_chart_template() -> None:
    """`helm template` should render service and deployment manifests."""
    chart_dir = Path("charts/scdocbuilder")
    result = subprocess.run(
        ["helm", "template", "scdocbuilder", str(chart_dir)],
        capture_output=True,
        text=True,
        cwd=chart_dir,
    )
    out = result.stdout.lower()
    assert "kind: service" in out
    assert "kind: deployment" in out
