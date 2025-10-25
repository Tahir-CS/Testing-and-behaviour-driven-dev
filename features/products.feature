Feature: Administrative product management UI
  As an admin user
  I want to manage products in the catalog
  So that the eCommerce app has an up-to-date product catalog

  Background:
    Given the service is running
    And the catalog is initialized with sample products

  Scenario: Create a Product
    When I create a new product named "Widget" in category "Gadgets" that is available
    Then I should see "Widget" in the product list

  Scenario: Read a Product
    Given a product named "Alpha" exists
    When I view the details for product "Alpha"
    Then I should see the product details for "Alpha"

  Scenario: Update a Product
    Given a product named "Alpha" exists
    When I rename product "Alpha" to "Alpha-2"
    Then I should see the product name as "Alpha-2"

  Scenario: Delete a Product
    Given a product named "Beta" exists
    When I delete product "Beta"
    Then product "Beta" should not appear in the list

  Scenario: List by Category
    When I filter products by category "A"
    Then I should see only products in category "A"

  Scenario: List by Available
    When I filter products by availability "true"
    Then I should see only available products

  Scenario: List by Name
    When I search products by name containing "alp"
    Then I should see products with names containing "alp"
