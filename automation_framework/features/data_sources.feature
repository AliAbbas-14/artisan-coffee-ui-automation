Feature: Multi-Source Test Data Integration (Excel, DB, Redis)
  As a QA Automation Engineer
  I want the framework to dynamically consume test datasets from Excel spreadsheets, SQLite DB, and Redis
  So that the testing suite demonstrates modular, enterprise-grade test data management

  Background:
    Given the user navigates to the Artisan Coffee website

  @datadriven @excel
  Scenario: Validate menu items using test data loaded from Excel spreadsheet
    Given test data is loaded from Excel sheet "MenuProducts" for scenario "TC_PRD_01"
    Then the UI menu should feature the coffee item specified in the Excel dataset

  @datadriven @database
  Scenario: Validate menu items using records queried directly from SQLite database
    Given test records are queried from the SQLite database table "CoffeeMenu"
    Then the UI menu should display the products fetched from the database

  @datadriven @redis
  Scenario: Validate menu items using cached test data fetched from Redis
    Given test criteria is fetched from Redis cache key "cache:menu:signature"
    Then the UI menu should display the cached coffee items
