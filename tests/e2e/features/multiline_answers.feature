Feature: Epic 3: Placeholder Replacement Logic
  Scenario: Handle multiline answers by reading the paragraph following the prompt
    Given a worksheet answer spans multiple lines
    When fields are extracted
    Then the entire multiline answer is captured correctly
