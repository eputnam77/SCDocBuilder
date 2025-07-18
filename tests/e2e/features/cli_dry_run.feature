Feature: Epic 2: CLI Implementation
  Scenario: Add --dry-run flag that prints a JSON diff instead of writing a file
    Given the user runs the CLI with --dry-run
    When processing completes
    Then a JSON diff is printed to stdout and no file is written
