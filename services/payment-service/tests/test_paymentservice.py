import pytest
from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from src.main import app, get_db
from src.models import Payment, Refund, Dispute, User

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

def test_create_payment(client, mock_db_session):
    def mock_refresh(instance):
        instance.id = 1
        instance.status = "completed"
    mock_db_session.refresh.side_effect = mock_refresh

    # Mock user query to return None (trigger auto-creation) OR return a mock user
    # Let's return None to test the auto-create flow? Or return mock user.
    # The code: if user is None: create user.
    # Let's mock finding a user to keep it simple.
    mock_user = User(id=1, name="Test", email="test@test.com")
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_user

    payload = {
        "user_id": 1,
        "amount": 100.00
    }
    
    response = client.post("/api/payments", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["amount"] == 100.0
    assert "id" in data
    
    mock_db_session.add.assert_called()
    mock_db_session.commit.assert_called()

def test_get_payment(client, mock_db_session):
    mock_payment = Payment(id=1, user_id=1, amount=100.0, status="completed")
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_payment
    
    response = client.get("/api/payments/1")
    assert response.status_code == 200
    assert response.json()["status"] == "completed"

def test_update_payment_status(client, mock_db_session):
    mock_payment = Payment(id=1, user_id=1, amount=100.0, status="pending")
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_payment
    
    response = client.patch("/api/payments/1?status=completed")
    assert response.status_code == 200
    assert response.json()["status"] == "updated"
    assert mock_payment.status == "completed"

def test_get_payment_history(client, mock_db_session):
    mock_payment = Payment(id=1, user_id=1, amount=100.0, status="completed")
    mock_db_session.query.return_value.filter.return_value.all.return_value = [mock_payment]
    
    response = client.get("/api/payments/history/1")
    assert response.status_code == 200
    assert len(response.json()) == 1

def test_create_refund(client, mock_db_session):
    mock_payment = Payment(id=1, user_id=1, amount=100.0, status="completed")
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_payment
    
    def mock_refresh(instance):
        instance.id = 1
    mock_db_session.refresh.side_effect = mock_refresh

    payload = {"payment_id": 1, "reason": "Defective"}
    response = client.post("/api/refunds", json=payload)
    
    assert response.status_code == 200
    assert "refund_id" in response.json()

def test_create_dispute(client, mock_db_session):
    mock_payment = Payment(id=1, user_id=1, amount=100.0, status="completed")
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_payment
    
    def mock_refresh(instance):
        instance.id = 1
    mock_db_session.refresh.side_effect = mock_refresh

    payload = {"payment_id": 1, "description": "Unauthorized"}
    response = client.post("/api/disputes", json=payload)
    
    assert response.status_code == 200
    assert "dispute_id" in response.json()
