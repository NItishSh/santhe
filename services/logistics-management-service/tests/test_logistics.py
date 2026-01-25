import pytest
from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from datetime import datetime
from src.main import app, get_db
from src.models import Delivery, Shipping

# --- Fixtures ---

@pytest.fixture
def mock_db_session():
    """Returns a mock implementation of the SQLAlchemy Session."""
    session = MagicMock()
    
    def side_effect_refresh(obj):
        if hasattr(obj, 'id') and not obj.id:
            obj.id = 1
        if hasattr(obj, 'timestamp') and not obj.timestamp:
            obj.timestamp = datetime.utcnow()
        if hasattr(obj, 'status') and not obj.status:
            obj.status = "pending"
            
    session.refresh.side_effect = side_effect_refresh
    return session

@pytest.fixture
def client(mock_db_session):
    def override_get_db():
        try:
            yield mock_db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides = {}

# --- Tests ---

def test_create_delivery(client, mock_db_session):
    payload = {"order_id": 123, "driver_id": 1, "location": "Warehouse"}
    response = client.post("/api/deliveries", json=payload)
    
    assert response.status_code == 201
    assert response.json()["order_id"] == 123
    assert response.json()["status"] == "pending"

def test_update_delivery(client, mock_db_session):
    mock_delivery = Delivery(id=1, order_id=123, driver_id=1, status="pending")
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_delivery
    
    payload = {"status": "in_transit", "location": "En route"}
    response = client.patch("/api/deliveries/1", json=payload)
    
    assert response.status_code == 200
    assert response.json()["status"] == "in_transit"
    assert mock_delivery.location == "En route"

def test_get_order_tracking_combined(client, mock_db_session):
    mock_delivery = Delivery(order_id=123, status="in_transit", location="City Center")
    mock_shipping = Shipping(order_id=123, carrier="FedEx", tracking_number="TRK123")
    
    # Mock multiple queries. First call for Delivery, second for Shipping
    # We can use side_effect or check call args logic.
    # But filtering by order_id is common.
    # The code queries: 
    #   delivery = db.query(Delivery).filter(...).first()
    #   shipping = db.query(Shipping).filter(...).first()
    
    def mock_query_side_effect(model):
        m = MagicMock()
        if model == Delivery:
            m.filter.return_value.first.return_value = mock_delivery
        elif model == Shipping:
            m.filter.return_value.first.return_value = mock_shipping
        return m
    
    mock_db_session.query.side_effect = mock_query_side_effect
    
    response = client.get("/api/orders/123/tracking")
    
    assert response.status_code == 200
    assert response.json()["status"] == "in_transit"
    assert response.json()["carrier"] == "FedEx"

def test_create_shipping(client, mock_db_session):
    payload = {"order_id": 123, "carrier": "DHL", "tracking_number": "123456"}
    response = client.post("/api/shipping", json=payload)
    
    assert response.status_code == 201
    assert response.json()["carrier"] == "DHL"

def test_update_location_coords(client, mock_db_session):
    mock_delivery = Delivery(id=1, order_id=123)
    # Reset side_effect if set globally or use a fresh mock
    # Here client uses the fixture which persists, so we might need to reset side_effect if we used it above.
    # Actually mock_db_session passed to this test is a fresh object if pytest scope is function (default).
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_delivery
    
    payload = {"order_id": 123, "latitude": 12.34, "longitude": 56.78}
    response = client.post("/api/location-updates", json=payload)
    
    assert response.status_code == 200
    assert mock_delivery.location == "12.34,56.78"
