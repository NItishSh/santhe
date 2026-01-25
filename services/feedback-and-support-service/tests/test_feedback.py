import pytest
from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from datetime import datetime
from src.main import app, get_db
from src.models import FeedbackTicket, Topic, Article

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
        if hasattr(obj, 'created_at') and not obj.created_at:
            obj.created_at = datetime.utcnow()
        if hasattr(obj, 'status') and not obj.status:
            obj.status = "open"
            
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

def test_create_support_ticket(client, mock_db_session):
    payload = {
        "user_id": 1,
        "subject": "Help",
        "description": "Login issue"
    }
    response = client.post("/api/support/tickets", json=payload)
    
    assert response.status_code == 201
    assert response.json()["status"] == "open"
    mock_db_session.add.assert_called()

def test_get_support_tickets_filter(client, mock_db_session):
    mock_ticket = FeedbackTicket(id=1, user_id=1, subject="Help", description="Login", status="open", timestamp=datetime.utcnow())
    mock_db_session.query.return_value.filter.return_value.filter.return_value.all.return_value = [mock_ticket]
    
    response = client.get("/api/support/tickets?status=open&user_id=1")
    
    assert response.status_code == 200
    assert len(response.json()) == 1

def test_close_support_ticket(client, mock_db_session):
    mock_ticket = FeedbackTicket(id=1, status="open")
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_ticket
    
    response = client.delete("/api/support/tickets/1")
    
    assert response.status_code == 200
    assert mock_ticket.status == "closed"

def test_submit_feedback(client, mock_db_session):
    payload = {
        "user_id": 1,
        "subject": "UI Improvement",
        "description": "Make it blue"
    }
    response = client.post("/api/feedback", json=payload)
    
    assert response.status_code == 201
    assert response.json()["subject"] == "[Feedback] UI Improvement"
    assert response.json()["status"] == "new"

def test_create_topic(client, mock_db_session):
    payload = {"name": "Account"}
    response = client.post("/api/knowledge-base/topics", json=payload)
    
    assert response.status_code == 200
    assert response.json()["name"] == "Account"

def test_list_articles(client, mock_db_session):
    mock_article = Article(id=1, topic_id=1, title="Reset Password", content="Click here", created_at=datetime.utcnow())
    mock_db_session.query.return_value.filter.return_value.all.return_value = [mock_article]
    
    response = client.get("/api/knowledge-base/articles/1")
    
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "Reset Password"

def test_support_stubs(client):
    response = client.post("/api/support/chat", json={"user_id": 1, "message": "Hi"})
    assert response.status_code == 200
    assert "session_id" in response.json()
