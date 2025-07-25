# Performance Optimization Report

A short profiling run was executed with `cProfile` on the CLI using temporary DOCX files. The run completed in ~0.18s (116k calls) with most time spent inside `python-docx` XML parsing and compression functions.

No API server was running and the project does not use a database or bundle any frontend assets, so k6 testing and bundle size inspection were skipped.

## Safe to try

### Recommendation: Cache placeholder schema loading
- Impact: Low (avoids repeated disk reads)
- Effort: Low
- Risk: Low
- Priority: P1
- ready-for:builder

## Review needed

### Recommendation: Parallelize batch processing
- Impact: Moderate when many worksheets are processed
- Effort: Moderate (use `concurrent.futures`)
- Risk: Moderate (concurrency issues)
- Priority: P3
- ready-for:builder

### Recommendation: Stream large DOCX files instead of loading entirely
- Impact: Moderate (reduced memory usage)
- Effort: High (requires lower level API)
- Risk: High
- Priority: P3
- ready-for:builder

### Recommendation: Implement profiling CI
- Impact: Low (visibility into regressions)
- Effort: Moderate
- Risk: Low
- Priority: P2
- ready-for:builder
