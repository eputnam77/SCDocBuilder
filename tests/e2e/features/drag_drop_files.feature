Feature: Web drag and drop upload
  Scenario: User uploads files via drag-and-drop and receives download link
    Given the user drags and drops a valid template and worksheet onto the upload area
    When the files are processed
    Then a progress bar is shown and the download link appears within five seconds
