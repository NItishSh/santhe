import pytest
from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from datetime import datetime
from src.main import app, get_db
from src.models import Payment, Refund, Dispute, User

# --- Fixtures ---

@pytest.fixture
def mock_db_session():
    """Returns a mock implementation of the SQLAlchemy Session."""
    session = MagicMock()
    
    def side_effect_refresh(obj):
        if hasattr(obj, 'id') and not obj.id:
            obj.id = 1
        if hasattr(obj, 'created_at') and not obj.created_at:
            obj.created_at = datetime.utcnow()
        if hasattr(obj, 'status') and not obj.status:
            obj.status = "completed" # simplistic default
            
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

# --- Tests for Payments ---

def test_create_payment_success(client, mock_db_session):
    # Mock user query
    mock_db_session.query.return_value.filter.return_value.first.return_value = User(id=1, name="Test", email="t@e.com")
    
    payload = {"user_id": 1, "amount": 100.0}
    response = client.post("/api/payments", json=payload)
    
    assert response.status_code == 201
    assert response.json()["amount"] == 100.0
    assert response.json()["status"] == "completed"

def test_get_payment_success(client, mock_db_session):
    mock_payment = Payment(id=1, user_id=1, amount=100.0, status="completed", created_at=datetime.utcnow())
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_payment
    
    response = client.get("/api/payments/1")
    
    assert response.status_code == 200
    assert response.json()["id"] == 1

def test_get_payment_not_found(client, mock_db_session):
    mock_db_session.query.return_value.filter.return_value.first.return_value = None
    response = client.get("/api/payments/999")
    assert response.status_code == 404

def test_get_payment_history(client, mock_db_session):
    mock_payment = Payment(id=1, user_id=1, amount=100.0, status="completed", created_at=datetime.utcnow())
    mock_db_session.query.return_value.filter.return_value.all.return_value = [mock_payment]
    
    response = client.get("/api/payments/history/1")
    
    assert response.status_code == 200
    assert len(response.json()) == 1

# --- Tests for Refunds ---

def test_create_refund_success(client, mock_db_session):
    mock_payment = Payment(id=1, user_id=1, amount=100.0, status="completed")
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_payment
    
    payload = {"payment_id": 1, "reason": "Defective"}
    response = client.post("/api/refunds", json=payload)
    
    assert response.status_code == 201
    assert response.json()["reason"] == "Defective"
    assert response.json()["status"] == "pending"

def test_create_refund_payment_not_found(client, mock_db_session):
    mock_db_session.query.return_value.filter.return_value.first.return_value = None
    
    payload = {"payment_id": 999, "reason": "Defective"}
    response = client.post("/api/refunds", json=payload)
    
    assert response.status_code == 404

# --- Tests for Disputes ---

def test_create_dispute_success(client, mock_db_session):
    mock_payment = Payment(id=1, user_id=1, amount=100.0, status="completed")
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_payment
    
    payload = {"payment_id": 1, "description": "Never received"}
    response = client.post("/api/disputes", json=payload)
    
    assert response.status_code == 201
    assert response.json()["status"] == "open"

