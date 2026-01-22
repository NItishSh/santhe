import pytest
from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from src.main import app, get_db
from src.models import Order as OrderModel

# --- Fixtures ---

@pytest.fixture
def mock_db_session():
    """Returns a mock implementation of the SQLAlchemy Session."""
    session = MagicMock()
    return session

@pytest.fixture
def client(mock_db_session):
    """
    Returns a TestClient with the `get_db` dependency overridden 
    to return our mock session.
    """
    def override_get_db():
        try:
            yield mock_db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    # Clean up override
    app.dependency_overrides = {}

# --- Tests ---

def test_create_order(client, mock_db_session):
    # Mock db.refresh logic (simulate ID generation)
    def mock_refresh(instance):
        instance.order_id = 1
    
    mock_db_session.refresh.side_effect = mock_refresh

    payload = {
        "farmer_id": 1,
        "middleman_id": 2,
        "product_id": 3,
        "quantity": 10
    }
    
    response = client.post("/api/orders", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert "order_id" in data
    assert data["order_id"] == 1
    assert data["status"] == "pending"

    mock_db_session.add.assert_called()
    mock_db_session.commit.assert_called()

def test_get_orders(client, mock_db_session):
    # Mock query returning list
    mock_order = OrderModel(order_id=1, farmer_id=1, middleman_id=2, product_id=3, quantity=10, status="pending")
    mock_db_session.query.return_value.all.return_value = [mock_order]

    response = client.get("/api/orders")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["order_id"] == 1

def test_get_order(client, mock_db_session):
    mock_order = OrderModel(order_id=1, farmer_id=1, middleman_id=2, product_id=3, quantity=10, status="pending")
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_order

    response = client.get("/api/orders/1")
    
    assert response.status_code == 200
    assert response.json()["order_id"] == 1

def test_get_order_not_found(client, mock_db_session):
    mock_db_session.query.return_value.filter.return_value.first.return_value = None
    response = client.get("/api/orders/999")
    assert response.status_code == 404

def test_update_order(client, mock_db_session):
    mock_order = OrderModel(order_id=1, farmer_id=1, middleman_id=2, product_id=3, quantity=10, status="pending")
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_order

    response = client.patch("/api/orders/1", json={"status": "in_progress"})
    
    assert response.status_code == 200
    assert response.json()["status"] == "in_progress"
    # Ensure modification happened on the mock object
    assert mock_order.status == "in_progress"
    mock_db_session.commit.assert_called()

def test_delete_order(client, mock_db_session):
    mock_order = OrderModel(order_id=1, status="pending")
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_order

    response = client.delete("/api/orders/1")
    
    assert response.status_code == 200
    assert response.json() == {"message": "Order deleted successfully"}
    mock_db_session.delete.assert_called_with(mock_order)
    mock_db_session.commit.assert_called()

def test_get_orders_status(client, mock_db_session):
    mock_order = OrderModel(order_id=1, status="pending")
    mock_db_session.query.return_value.all.return_value = [mock_order]

    response = client.get("/api/orders/status")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert data[0]["order_id"] == 1
    assert data[0]["status"] == "pending"
