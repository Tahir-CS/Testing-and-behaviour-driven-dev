from http import HTTPStatus

from app import db
from app.models import Product
from tests.factories import create_product, fake_product_payload


def test_model_create_read_update_delete(app):  # uses app context fixture
    # CREATE
    p = create_product(name="ModelItem", category="A", available=True)
    assert p.id is not None

    # READ
    got = Product.query.get(p.id)
    assert got is not None
    assert got.name == "ModelItem"

    # UPDATE
    got.name = "ModelItem-2"
    got.available = False
    db.session.commit()

    again = Product.query.get(p.id)
    assert again is not None
    assert again.name == "ModelItem-2"
    assert again.available is False

    # DELETE
    db.session.delete(again)
    db.session.commit()
    assert Product.query.get(p.id) is None


def test_model_list_all_and_filters(app):
    # seed products
    a1 = create_product(name="Alpha", category="A", available=True)
    b1 = create_product(name="Beta", category="B", available=False)
    a2 = create_product(name="Gamma", category="A", available=True)
    a3 = create_product(name="alphabet", category="C", available=True)

    # LIST ALL
    all_items = Product.query.order_by(Product.id.asc()).all()
    assert len(all_items) >= 4

    # FIND BY NAME (contains, case-insensitive via Python)
    name_items = [p for p in all_items if "alpha" in p.name.lower()]
    assert {p.name for p in name_items} == {"Alpha", "alphabet"}

    # FIND BY CATEGORY
    cat_a = Product.query.filter(Product.category == "A").all()
    assert {p.name for p in cat_a} >= {"Alpha", "Gamma"}

    # FIND BY AVAILABILITY
    avail_true = Product.query.filter(Product.available.is_(True)).all()
    assert all(p.available for p in avail_true)
