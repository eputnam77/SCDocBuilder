Feature: Epic 4: Web Interface
  Scenario: Upload and download completes within five seconds
    Given the user uploads a valid worksheet and template via the web UI
    When the notice is generated
    Then the download link is provided within five seconds
