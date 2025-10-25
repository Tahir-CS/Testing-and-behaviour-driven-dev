# NOTE: These steps are designed to interact with the provided UI in Part 2 using Selenium.
# Since the UI is not present in this workspace, these steps are stubs that call the API
# directly, which allows the scenarios to run against the service. Replace these with
# real Selenium UI interactions when you add the admin UI.

import os

from behave import given, then, when
import requests

BASE_URL = os.getenv("BASE_URL", "http://localhost:5000")


@given('a product named "{name}" exists')
def step_product_exists(context, name):
    requests.post(f"{BASE_URL}/products", json={"name": name}, timeout=5)


@when('I view the details for product "{name}"')
def step_view_product_details(context, name):
    resp = requests.get(f"{BASE_URL}/products", params={"name": name}, timeout=5)
    items = resp.json()
    assert items
    context.product_id = items[0]["id"]


@when('I create a new product named "{name}" in category "{category}" that is available')
def step_create_product(context, name, category):
    context.last_resp = requests.post(
        f"{BASE_URL}/products",
        json={"name": name, "category": category, "available": True},
        timeout=5,
    )


@then('I should see "{name}" in the product list')
def step_see_product_in_list(context, name):
    resp = requests.get(f"{BASE_URL}/products", timeout=5)
    assert any(p["name"] == name for p in resp.json())


@then('I should see the product details for "{name}"')
def step_assert_details(context, name):
    resp = requests.get(f"{BASE_URL}/products/{context.product_id}", timeout=5)
    assert resp.status_code == 200
    assert resp.json()["name"] == name


@when('I rename product "{old}" to "{new}"')
def step_rename_product(context, old, new):
    resp = requests.get(f"{BASE_URL}/products", params={"name": old}, timeout=5)
    items = resp.json()
    assert items
    pid = items[0]["id"]
    context.last_resp = requests.put(
        f"{BASE_URL}/products/{pid}", json={"name": new}, timeout=5
    )


@then('I should see the product name as "{name}"')
def step_assert_name(context, name):
    assert context.last_resp.status_code in (200, 201)
    assert context.last_resp.json()["name"] == name


@then('I should see the product name as "{name}"')
def step_assert_name(context, name):
    assert context.last_resp.status_code in (200, 201)
    assert context.last_resp.json()["name"] == name


@when('I delete product "{name}"')
def step_delete_product(context, name):
    resp = requests.get(f"{BASE_URL}/products", params={"name": name}, timeout=5)
    items = resp.json()
    assert items
    pid = items[0]["id"]
    context.last_resp = requests.delete(f"{BASE_URL}/products/{pid}", timeout=5)


@then('product "{name}" should not appear in the list')
def step_not_in_list(context, name):
    resp = requests.get(f"{BASE_URL}/products", timeout=5)
    assert not any(p["name"] == name for p in resp.json())


@when('I filter products by category "{category}"')
def step_filter_category(context, category):
    context.last_resp = requests.get(
        f"{BASE_URL}/products", params={"category": category}, timeout=5
    )


@then('I should see only products in category "{category}"')
def step_assert_category(context, category):
    assert context.last_resp.status_code == 200
    assert all(p.get("category") == category for p in context.last_resp.json())


@when('I filter products by availability "{available}"')
def step_filter_available(context, available):
    context.last_resp = requests.get(
        f"{BASE_URL}/products", params={"available": available}, timeout=5
    )


@then("I should see only available products")
def step_assert_available_true(context):
    assert context.last_resp.status_code == 200
    assert all(p.get("available") for p in context.last_resp.json())


@when('I search products by name containing "{token}"')
def step_search_name(context, token):
    context.last_resp = requests.get(
        f"{BASE_URL}/products", params={"name": token}, timeout=5
    )


@then('I should see products with names containing "{token}"')
def step_assert_name_contains(context, token):
    assert context.last_resp.status_code == 200
    assert all(token.lower() in p.get("name", "").lower() for p in context.last_resp.json())
