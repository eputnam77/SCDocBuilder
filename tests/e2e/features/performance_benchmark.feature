Feature: Epic 6: Performance
  Scenario: Benchmark processing under one second for typical file sizes
    Given a 500 KB template and a 1 MB worksheet
    When the benchmark utility runs
    Then the processing completes in under one second
