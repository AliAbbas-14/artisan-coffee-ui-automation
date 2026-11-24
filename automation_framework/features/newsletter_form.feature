Feature: Newsletter Subscription Form Automation
  As a customer of Artisan Coffee
  I want to submit my email to the Coffee Letter newsletter
  So that I receive exclusive roasts and coffee brewing guides

  Background:
    Given the user navigates to the Artisan Coffee website

  @smoke @forms
  Scenario: Verify newsletter subscription form elements
    Then the newsletter subscription form should be visible
    And the email input field and subscribe button should be ready for input

  @regression @forms @datadriven
  Scenario Outline: Data-Driven Newsletter Subscription with Multiple Email Formats
    When the user enters "<email>" into the newsletter subscription input
    Then the email input field should contain "<email>"
    And the user clicks the subscribe button

    Examples:
      | email                             | note                     |
      | ali.abbas.tester@gmail.com        | Standard Gmail address   |
      | artisan.barista2026@outlook.com   | Outlook corporate email  |
      | qa_lead_automation@fast.edu.pk    | Academic student domain  |
