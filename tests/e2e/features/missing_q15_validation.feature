Feature: Epic 2: CLI Implementation
  Scenario: Missing Q15 answer exits with EVALID
    Given a worksheet missing the answer to question 15
    When the CLI processes the worksheet
    Then it exits with code EVALID and prints a clear message
