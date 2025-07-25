import runpy
from typing import Any
import typing
import pytest

if not typing.TYPE_CHECKING:
    pytest.importorskip("docx")


def test_module_entrypoint(monkeypatch: Any) -> None:
    called = []

    def fake_main(argv: list[str] | None = None) -> None:
        called.append(True)

    monkeypatch.setattr("scdocbuilder.cli.main", fake_main)
    runpy.run_module("scdocbuilder.__main__", run_name="__main__")
    assert called
