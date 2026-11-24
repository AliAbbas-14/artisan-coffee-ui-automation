Feature: The Blend Lab Flavour Profiles
  As a customer looking for custom artisan roasts
  I want to explore the Blend Lab flavour decoders and place orders
  So that I can enjoy signature roast combinations

  Background:
    Given the user navigates to the Artisan Coffee website

  @regression @blend
  Scenario: Explore the Blend Lab section
    When the user navigates to the Blend Lab section
    Then the Blend Lab section should be visible

  @regression @blend @datadriven
  Scenario Outline: Select and order signature roast blends
    When the user navigates to the Blend Lab section
    Then the order button for blend "<blend_name>" should be available

    Examples:
      | blend_name     |
      | ESPRESSO NOIR  |
      | MORNING GOLD   |
      | VELVET HOUR    |
