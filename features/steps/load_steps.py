import os

import requests
from behave import given

BASE_URL = os.getenv("BASE_URL", "http://localhost:5000")


@given("the service is running")
def step_service_running(context):
    resp = requests.get(f"{BASE_URL}/health", timeout=5)
    assert resp.status_code == 200


@given("the catalog is initialized with sample products")
def step_seed_catalog(context):
    # seed a few products idempotently
    for name, category, available in [
        ("Alpha", "A", True),
        ("Beta", "B", False),
        ("Gamma", "A", True),
    ]:
        requests.post(
            f"{BASE_URL}/products",
            json={"name": name, "category": category, "available": available},
            timeout=5,
        )
