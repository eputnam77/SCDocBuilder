# Performance Optimization Report

This audit reviews the current CLI-based application for filling FAA Special Condition templates.
The project has no running API or frontend, so k6 and Lighthouse were not applicable.
Profiling with `py-spy` on a sample run indicated most time spent inside placeholder replacement loops.

## Safe to try

### Recommendation: Remove unused imports flagged by Ruff
- Expected Impact: Low (slightly faster startup and cleaner code)
- Effort: Trivial
- Breakage Risk: Safe
- Dependencies: None
- Priority: P1 (quick win)
- ready-for:builder

### Recommendation: Precompile conditional regex in `apply_conditionals`
- Expected Impact: Low (avoid recompiling pattern each call)
- Effort: Low
- Breakage Risk: Low
- Dependencies: None
- Priority: P2
- ready-for:builder

### Recommendation: Cache placeholder schema loading
- Expected Impact: Moderate (avoids disk reads on repeated runs)
- Effort: Low
- Breakage Risk: Low
- Dependencies: None
- Priority: P2
- ready-for:builder

## Review needed

### Recommendation: Parallelize batch processing
- Expected Impact: Moderate to High when processing many worksheets
- Effort: Moderate (use `concurrent.futures`)
- Breakage Risk: Moderate (concurrency issues)
- Dependencies: Requires batch mode implementation
- Priority: P3
- ready-for:builder

### Recommendation: Stream large DOCX files instead of loading entirely
- Expected Impact: Moderate (reduced memory usage)
- Effort: High (requires different library or lower level API)
- Breakage Risk: High
- Dependencies: Testing with large files
- Priority: P3
- ready-for:builder

### Recommendation: Implement profiling CI step
- Expected Impact: Low (visibility into regressions)
- Effort: Moderate
- Breakage Risk: Safe
- Dependencies: Setup py-spy and pytest-benchmark
- Priority: P2
- ready-for:builder
