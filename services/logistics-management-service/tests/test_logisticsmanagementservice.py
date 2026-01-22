import pytest
from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from src.main import app, get_db
from src.models import Delivery

# --- Fixtures ---

@pytest.fixture
def mock_db_session():
    """Returns a mock implementation of the SQLAlchemy Session."""
    session = MagicMock()
    return session

@pytest.fixture
def client(mock_db_session):
    """
    Returns a TestClient with the `get_db` dependency overridden.
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

def test_create_delivery(client, mock_db_session):
    def mock_refresh(instance):
        instance.id = 1
        instance.status = "pending"
        instance.timestamp = "2023-01-01T00:00:00"
    mock_db_session.refresh.side_effect = mock_refresh

    payload = {
        "order_id": 101,
        "location": "Warehouse A"
    }
    
    response = client.post("/api/deliveries", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["order_id"] == 101
    assert data["status"] == "pending"
    assert "id" in data
    
    mock_db_session.add.assert_called()
    mock_db_session.commit.assert_called()

def test_get_delivery(client, mock_db_session):
    mock_delivery = Delivery(id=1, order_id=101, status="in_transit", location="En route", timestamp="2023-01-01T00:00:00")
    
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_delivery
    
    response = client.get("/api/deliveries/1")
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "in_transit"

def test_update_delivery(client, mock_db_session):
    mock_delivery = Delivery(id=1, order_id=101, status="pending", location="Warehouse A", timestamp="2023-01-01T00:00:00")
    
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_delivery
    
    payload = {"status": "delivered", "driver_id": 505}
    response = client.patch("/api/deliveries/1", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "delivered"
    assert data["driver_id"] == 505
    
    assert mock_delivery.status == "delivered"
    assert mock_delivery.driver_id == 505
    mock_db_session.commit.assert_called()