from faa_sc_replacer.cli import parse_args


def test_parse_args_parses_required() -> None:
    args = parse_args(
        [
            "--template",
            "t.docx",
            "--worksheet",
            "w.docx",
            "--dry-run",
            "--log-level",
            "DEBUG",
        ]
    )
    assert args.template == "t.docx"
    assert args.worksheet == "w.docx"
    assert args.dry_run is True
    assert args.log_level == "DEBUG"
