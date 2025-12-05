
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_list_products():
    r = client.get("/products")
    assert r.status_code == 200
    assert isinstance(r.json(), list)


def test_create_get_update_delete_product():
    # Create
    r = client.post("/products", json={"name": "Webcam", "price": 50.0, "in_stock": True})
    assert r.status_code == 201
    pid = r.json()["id"]

    # Get
    r = client.get(f"/products/{pid}")
    assert r.status_code == 200
    assert r.json()["name"] == "Webcam"

    # Update
    r = client.put(f"/products/{pid}", json={"price": 55.0})
    assert r.status_code == 200
    assert r.json()["price"] == 55.0

    # Delete
    r = client.delete(f"/products/{pid}")
    assert r.status_code == 204

    # Verify deletion
    r = client.get(f"/products/{pid}")
    assert r.status_code == 404
