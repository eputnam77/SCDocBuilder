Feature: Epic 4: HTML Export
  Scenario: CLI flag generates sanitized HTML using mammoth and bleach
    Given a completed document
    When the user invokes the CLI with --html-out OUTPUT.html
    Then sanitized HTML is written to that path

  Scenario: API returns sanitized HTML when requested
    Given the API receives template and worksheet files
    When the client requests HTML output
    Then the response contains sanitized HTML content
