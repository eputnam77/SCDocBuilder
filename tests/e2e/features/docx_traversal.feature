Feature: Epic 3: Placeholder Replacement Logic
  Scenario: Traverse paragraphs, tables, headers, footers, numbered lists and textboxes for placeholders
    Given a template containing placeholders in all document parts
    When placeholders are replaced
    Then no unreplaced placeholders remain anywhere in the document
