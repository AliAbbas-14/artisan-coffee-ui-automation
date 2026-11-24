Feature: Signature Coffee Menu Catalog
  As a coffee enthusiast
  I want to review the signature roast menu and detailed tasting profiles
  So that I can select my preferred brew origin and roast intensity

  Background:
    Given the user navigates to the Artisan Coffee website
    When the user navigates to the signature menu section

  @smoke @menu
  Scenario: Verify signature menu header and products availability
    Then the signature menu header should be displayed
    And the menu should feature "Black Label Espresso"
    And the menu should feature "Velvet Oat Latte"
    And the menu should feature "Midnight Cold Brew"

  @regression @menu
  Scenario Outline: Verify specific signature coffee details
    Then the menu should feature "<coffee_name>"
    And the coffee origin "<origin>" should be displayed in the menu

    Examples:
      | coffee_name          | origin                         |
      | Black Label Espresso | COLOMBIA · HUILA · WASHED      |
      | Velvet Oat Latte     | ETHIOPIA · YIRGACHEFFE · NATURAL|
      | Midnight Cold Brew   | GUATEMALA · ANTIGUA · HONEY    |
