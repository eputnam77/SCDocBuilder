# Repository Structure

```
├── src/                # application code
│   └── faa_sc_replacer/
├── tests/              # unit, property and e2e tests
├── manifests/          # deployment manifests
├── migrations/         # database migrations
├── scripts/            # helper scripts
├── ADR/                # architecture decision records
├── .github/workflows/  # CI configuration
├── .dev/               # planning docs (not packaged)
```

The `src/` layout isolates import paths during tests. `manifests/` and `migrations/` provide a place for deployment files and schema changes. ADRs live in `ADR/` for easy reference.
