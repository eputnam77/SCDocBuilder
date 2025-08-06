Feature: Web keyboard navigation
  Scenario: User navigates upload, preview, and download controls via keyboard
    Given the web interface is open
    When the user presses the Tab key repeatedly
    Then focus reaches the upload input, preview button, and download link in order
