Feature: Epic 2: CLI Implementation
  Scenario: Add minimal logging with configurable level
    Given the user sets the log level to DEBUG
    When the CLI runs
    Then debug messages are emitted to the log output
