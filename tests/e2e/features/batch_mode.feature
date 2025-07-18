Feature: Epic 2: CLI Implementation
  Scenario: Optional batch mode to process all worksheets in a directory
    Given the user supplies a directory of worksheets
    When batch mode is invoked
    Then the CLI generates a notice for each worksheet in that directory
