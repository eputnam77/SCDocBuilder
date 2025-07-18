Feature: Epic 2: CLI Implementation
  Scenario: When --output is omitted, save as {template-stem}_{timestamp}.docx and print the path on stdout
    Given the user runs the CLI without specifying --output
    When processing completes successfully
    Then the output file is saved with a timestamped name and the path is printed
