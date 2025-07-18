Feature: Epic 2: CLI Implementation
  Scenario: Replace hard-coded file paths with an argparse CLI accepting --template and --worksheet (required) and --output (optional)
    Given the user runs the CLI with --template TEMPLATE and --worksheet WORKSHEET
    When the arguments are parsed
    Then the program loads the specified template and worksheet files
