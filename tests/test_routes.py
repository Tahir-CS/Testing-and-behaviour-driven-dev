from http import HTTPStatus


def test_read_product_route(client):
    created = client.post("/products", json={"name": "Item"}).get_json()
    pid = created["id"]
    got = client.get(f"/products/{pid}")
    assert got.status_code == HTTPStatus.OK
    assert got.get_json()["name"] == "Item"


def test_update_product_route(client):
    created = client.post("/products", json={"name": "Old", "available": True}).get_json()
    pid = created["id"]
    update = client.put(f"/products/{pid}", json={"name": "New", "available": False})
    assert update.status_code == HTTPStatus.OK
    body = update.get_json()
    assert body["name"] == "New"
    assert body["available"] is False


def test_delete_product_route(client):
    created = client.post("/products", json={"name": "DeleteMe"}).get_json()
    pid = created["id"]
    resp = client.delete(f"/products/{pid}")
    assert resp.status_code == HTTPStatus.NO_CONTENT
    assert client.get(f"/products/{pid}").status_code == HTTPStatus.NOT_FOUND


def _seed(client):
    items = [
        {"name": "Alpha", "category": "A", "available": True},
        {"name": "Beta", "category": "B", "available": False},
        {"name": "Gamma", "category": "A", "available": True},
        {"name": "alphabet", "category": "C", "available": True},
    ]
    for it in items:
        client.post("/products", json=it)


def test_list_all_route(client):
    _seed(client)
    resp = client.get("/products")
    assert resp.status_code == HTTPStatus.OK
    assert len(resp.get_json()) >= 4


def test_list_by_name_route(client):
    _seed(client)
    data = client.get("/products?name=alpha").get_json()
    assert {x["name"] for x in data} == {"Alpha", "alphabet"}


def test_list_by_category_route(client):
    _seed(client)
    data = client.get("/products?category=A").get_json()
    assert {x["name"] for x in data} == {"Alpha", "Gamma"}


def test_list_by_availability_route(client):
    _seed(client)
    t = client.get("/products?available=true").get_json()
    assert all(x["available"] for x in t)
    f = client.get("/products?available=false").get_json()
    assert all(not x["available"] for x in f)
