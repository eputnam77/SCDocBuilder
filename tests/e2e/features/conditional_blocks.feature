Feature: Epic 3: Placeholder Replacement Logic
  Scenario: Implement Worksheet #6 conditional blocks keeping only the selected option
    Given a template containing OPTION blocks for worksheet question 6
    When the user selects option 2
    Then only OPTION_2 text remains and the others are removed
