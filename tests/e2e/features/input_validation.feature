Feature: Epic 2: CLI Implementation
  Scenario: Validate file existence, extension, and size before processing
    Given the user provides template and worksheet paths
    When the files are missing or invalid
    Then the CLI exits with a descriptive error code
