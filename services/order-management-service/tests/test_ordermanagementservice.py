# tests/test_inventory.py

import pytest
from fastapi.testclient import TestClient
from src.main import app

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

def test_create_order(client):
    order_data = {
        "farmer_id": 1,
        "middleman_id": 2,
        "product_id": 3,
        "quantity": 10
    }
    response = client.post("/api/orders", json=order_data)
    assert response.status_code == 200
    assert "order_id" in response.json()

def test_get_orders(client):
    response = client.get("/api/orders")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_order(client):
    order_data = {
        "farmer_id": 1,
        "middleman_id": 2,
        "product_id": 3,
        "quantity": 10
    }
    create_response = client.post("/api/orders", json=order_data)
    order_id = create_response.json()["order_id"]
    
    response = client.get(f"/api/orders/{order_id}")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert response.json()["order_id"] == order_id

def test_update_order_status(client):
    order_data = {
        "farmer_id": 1,
        "middleman_id": 2,
        "product_id": 3,
        "quantity": 10
    }
    create_response = client.post("/api/orders", json=order_data)
    order_id = create_response.json()["order_id"]
    
    update_data = {"status": "in_progress"}
    response = client.patch(f"/api/orders/{order_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["status"] == "in_progress"

def test_delete_order(client):
    order_data = {
        "farmer_id": 1,
        "middleman_id": 2,
        "product_id": 3,
        "quantity": 10
    }
    create_response = client.post("/api/orders", json=order_data)
    order_id = create_response.json()["order_id"]
    
    response = client.delete(f"/api/orders/{order_id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Order deleted successfully"}

def test_get_orders_status(client):
    response = client.get("/api/orders/status")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_order_status(client):
    order_data = {
        "farmer_id": 1,
        "middleman_id": 2,
        "product_id": 3,
        "quantity": 10
    }
    create_response = client.post("/api/orders", json=order_data)
    order_id = create_response.json()["order_id"]
    
    response = client.get(f"/api/orders/{order_id}/status")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert response.json()["order_id"] == order_id

def test_send_notification(client):
    notification_data = {"message": "Test notification"}
    response = client.post("/api/notifications", json=notification_data)
    assert response.status_code == 200
    assert response.json() == {"message": "Notification sent successfully"}
