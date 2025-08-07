# SCDocBuilder

Fill FAA Special Conditions templates with worksheet answers.

## What

SCDocBuilder reads your worksheet and writes a polished Special Conditions
notice. It handles table fields, conditional blocks and multiline responses.

## Why

You avoid manual editing and stay consistent with AIR-646 style in seconds.

## How

* CLI: `python -m scdocbuilder`
* FastAPI: `uvicorn scdocbuilder.api:app`
* Library: call functions in [`docs/api/python.md`](docs/api/python.md)

See [`docs/scenarios.md`](docs/scenarios.md) for step-by-step tasks.

## Quick start

```bash
python -m pip install scdocbuilder
python -m scdocbuilder --template template.docx --worksheet worksheet.docx
```

## Contributing

* `poetry install --with dev`
* `pre-commit run --files <changed-files>`
* `pytest -q`

## License

GNU General Public License v3.0. See [LICENSE](LICENSE).
