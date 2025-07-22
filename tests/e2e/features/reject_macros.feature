Feature: Epic 7: Security
  Scenario: Macro-enabled documents are rejected
    Given an uploaded DOCM file
    When macro detection runs
    Then the file is rejected with an error

  Scenario: Uploaded files are deleted after processing
    Given files were uploaded for generation
    When processing completes
    Then the uploaded files no longer exist on disk
