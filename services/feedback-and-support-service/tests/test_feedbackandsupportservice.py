import pytest
from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from src.main import app, get_db
from src.models import FeedbackTicket

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

def test_create_ticket(client, mock_db_session):
    def mock_refresh(instance):
        instance.id = 1
        instance.status = "open"
        instance.timestamp = "2023-01-01T00:00:00"
    mock_db_session.refresh.side_effect = mock_refresh

    payload = {
        "user_id": 1,
        "subject": "Login Issue",
        "description": "Cannot login"
    }
    
    response = client.post("/api/feedback", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["subject"] == "Login Issue"
    assert data["status"] == "open"
    assert "id" in data
    
    mock_db_session.add.assert_called()
    mock_db_session.commit.assert_called()

def test_get_tickets(client, mock_db_session):
    mock_ticket = FeedbackTicket(id=1, user_id=1, subject="Issue", description="Desc", status="open", timestamp="2023-01-01T00:00:00")
    
    mock_query = mock_db_session.query.return_value
    mock_query.filter.return_value = mock_query
    mock_query.all.return_value = [mock_ticket]
    
    response = client.get("/api/feedback?status=open")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["subject"] == "Issue"

def test_update_ticket(client, mock_db_session):
    mock_ticket = FeedbackTicket(id=1, user_id=1, subject="Issue", description="Desc", status="open", timestamp="2023-01-01T00:00:00")
    
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_ticket
    
    payload = {"status": "resolved"}
    response = client.patch("/api/feedback/1", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "resolved"
    
    assert mock_ticket.status == "resolved"
    mock_db_session.commit.assert_called()