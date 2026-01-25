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
    
    def side_effect_refresh(obj):
        if not hasattr(obj, 'order_id') or not obj.order_id:
            obj.order_id = 1
        # Set default status if missing
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

def test_create_order(client, mock_db_session):
    payload = {
        "farmer_id": 1,
        "middleman_id": 2,
        "product_id": 10,
        "quantity": 50
    }
    response = client.post("/api/orders", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["farmer_id"] == 1
    assert data["status"] == "pending"
    mock_db_session.add.assert_called()
    mock_db_session.commit.assert_called()

def test_get_orders(client, mock_db_session):
    mock_orders = [
        OrderModel(order_id=1, farmer_id=1, middleman_id=2, product_id=10, quantity=50, status="pending")
    ]
    mock_db_session.query.return_value.all.return_value = mock_orders
    
    response = client.get("/api/orders")
    
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["order_id"] == 1

def test_get_order_by_id_success(client, mock_db_session):
    mock_order = OrderModel(order_id=1, farmer_id=1, middleman_id=2, product_id=10, quantity=50, status="pending")
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_order
    
    response = client.get("/api/orders/1")
    
    assert response.status_code == 200
    assert response.json()["order_id"] == 1

def test_get_order_by_id_not_found(client, mock_db_session):
    mock_db_session.query.return_value.filter.return_value.first.return_value = None
    
    response = client.get("/api/orders/999")
    
    assert response.status_code == 404

def test_update_order_status(client, mock_db_session):
    mock_order = OrderModel(order_id=1, farmer_id=1, middleman_id=2, product_id=10, quantity=50, status="pending")
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_order
    
    payload = {"status": "completed"}
    response = client.patch("/api/orders/1", json=payload)
    
    assert response.status_code == 200
    assert response.json()["status"] == "completed"
    # Verify modification
    assert mock_order.status == "completed"
    mock_db_session.commit.assert_called()

def test_delete_order(client, mock_db_session):
    mock_order = OrderModel(order_id=1)
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_order
    
    response = client.delete("/api/orders/1")
    
    assert response.status_code == 200
    mock_db_session.delete.assert_called_with(mock_order)
    mock_db_session.commit.assert_called()
