import runpy
from typing import Any


def test_module_entrypoint(monkeypatch: Any) -> None:
    called = []

    def fake_main(argv: list[str] | None = None) -> None:
        called.append(True)

    monkeypatch.setattr("faa_sc_replacer.cli.main", fake_main)
    runpy.run_module("faa_sc_replacer.__main__", run_name="__main__")
    assert called
