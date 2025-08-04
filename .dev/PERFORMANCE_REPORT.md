# Performance Report

## Profiling
- Attempted to run `cProfile` on the application, but module imports failed due to missing dependencies; profile artifacts are captured in `perf/artifacts/profile.pstats`.
- k6 API load testing could not be executed because installation failed (403 Forbidden). See `perf/artifacts/k6.txt`.

## Database Queries
- Searched project sources and found no database interactions; application operates solely on DOCX files.

## Bundle Size
- Source package size: 56K (`src/scdocbuilder`).

## Recommendations
| Recommendation | Impact | Effort | Risk | Priority |
|---|---|---|---|---|
| Cache default field mappings instead of recreating dict each call (implemented). | Low CPU savings for repeated calls | Low | Low | P1 |
| Use a combined regex to replace placeholders in single pass to reduce nested loops. | Medium throughput gain on large documents | Medium | Medium | P2 |
| Run FastAPI with `uvicorn` using multiple workers and `uvloop` in production. | Improved concurrency handling | Low | Low | P1 |
| Stream generated files instead of writing to disk before response. | Reduced I/O overhead for large documents | High | Medium | P3 |
