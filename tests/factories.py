"""Test factories for generating fake product data and instances."""

from __future__ import annotations

import random
import string
from typing import Dict

from app import db
from app.models import Product


def _rand_token(n: int = 6) -> str:
    return "".join(random.choices(string.ascii_letters, k=n))


def fake_product_payload(**overrides: object) -> Dict[str, object]:
    payload: Dict[str, object] = {
        "name": f"Product-{_rand_token()}",
        "category": random.choice(["A", "B", "C", None]),
        "available": random.choice([True, False]),
        "price": round(random.uniform(1.0, 100.0), 2),
        "description": "Auto-generated test product",
    }
    payload.update(overrides)
    return payload


def create_product(**overrides: object) -> Product:
    data = fake_product_payload(**overrides)
    product = Product(**data)  # type: ignore[arg-type]
    db.session.add(product)
    db.session.commit()
    return product
