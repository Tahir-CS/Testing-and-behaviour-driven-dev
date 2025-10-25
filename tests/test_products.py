from http import HTTPStatus


def test_health(client):
    resp = client.get("/health")
    assert resp.status_code == HTTPStatus.OK
    assert resp.get_json()["status"] == "ok"


def test_create_product_success(client):
    payload = {
        "name": "Widget",
        "category": "Gadgets",
        "available": True,
        "price": 19.99,
        "description": "A useful widget",
    }
    resp = client.post("/products", json=payload)
    assert resp.status_code == HTTPStatus.CREATED
    data = resp.get_json()
    assert data["id"] > 0
    assert data["name"] == "Widget"


def test_create_product_validation_error(client):
    payload = {"name": "   "}
    resp = client.post("/products", json=payload)
    assert resp.status_code == HTTPStatus.BAD_REQUEST


def test_get_product_and_not_found(client):
    # not found
    resp = client.get("/products/9999")
    assert resp.status_code == HTTPStatus.NOT_FOUND

    # create then get
    created = client.post("/products", json={"name": "Item"}).get_json()
    pid = created["id"]
    got = client.get(f"/products/{pid}")
    assert got.status_code == HTTPStatus.OK
    assert got.get_json()["name"] == "Item"


def test_update_product_success_and_not_found(client):
    # not found
    resp = client.put("/products/9999", json={"name": "New"})
    assert resp.status_code == HTTPStatus.NOT_FOUND

    # create then update
    created = client.post("/products", json={"name": "Old", "available": True}).get_json()
    pid = created["id"]

    update = client.put(f"/products/{pid}", json={"name": "New", "available": False})
    assert update.status_code == HTTPStatus.OK
    updated = update.get_json()
    assert updated["name"] == "New"
    assert updated["available"] is False


def test_delete_product_success_and_not_found(client):
    # not found
    assert client.delete("/products/9876").status_code == HTTPStatus.NOT_FOUND

    # create then delete
    created = client.post("/products", json={"name": "DeleteMe"}).get_json()
    pid = created["id"]

    resp = client.delete(f"/products/{pid}")
    assert resp.status_code == HTTPStatus.NO_CONTENT

    # ensure gone
    assert client.get(f"/products/{pid}").status_code == HTTPStatus.NOT_FOUND


def seed_products(client):
    items = [
        {"name": "Alpha", "category": "A", "available": True},
        {"name": "Beta", "category": "B", "available": False},
        {"name": "Gamma", "category": "A", "available": True},
        {"name": "alphabet", "category": "C", "available": True},
    ]
    for it in items:
        client.post("/products", json=it)


def test_list_products_filters(client):
    seed_products(client)

    # list all
    resp = client.get("/products")
    assert resp.status_code == HTTPStatus.OK
    all_items = resp.get_json()
    assert len(all_items) == 4

    # by category
    a = client.get("/products?category=A").get_json()
    assert {x["name"] for x in a} == {"Alpha", "Gamma"}

    # by available true
    avail_true = client.get("/products?available=true").get_json()
    assert all(x["available"] for x in avail_true)

    # by available false
    avail_false = client.get("/products?available=false").get_json()
    assert all(not x["available"] for x in avail_false)

    # by name contains (case-insensitive)
    name = client.get("/products?name=alpha").get_json()
    assert {x["name"] for x in name} == {"Alpha", "alphabet"}

    # invalid available filter
    bad = client.get("/products?available=maybe")
    assert bad.status_code == HTTPStatus.BAD_REQUEST
