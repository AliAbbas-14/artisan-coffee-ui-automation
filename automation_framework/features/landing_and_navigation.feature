Feature: Artisan Coffee Landing Page and Navigation
  As a visitor of the Artisan Coffee website
  I want to browse the hero banner, brand philosophy, and explore coffee collections
  So that I can experience the coffee shop interface and navigate seamlessly

  Background:
    Given the user navigates to the Artisan Coffee website

  @smoke @landing
  Scenario: Verify homepage hero banner and branding
    Then the brand logo "ARTISANCOFFEE" should be visible
    And the page title should contain "Artisan Coffee"
    And the hero rating badge should be displayed

  @smoke @navigation
  Scenario Outline: Test interactive navigation bar actions
    When the user clicks the navigation button "<nav_button>"
    Then the corresponding section "<section_id>" should be displayed

    Examples:
      | nav_button | section_id  |
      | MENU       | #menu       |
      | STORY      | #story      |
      | BLEND      | #blend      |
      | REVIEWS    | #reviews    |
      | LOCATIONS  | #locations  |
