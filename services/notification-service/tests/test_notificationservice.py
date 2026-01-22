import pytest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from src.main import app, get_db
from src.models import Notification, Preference
import uuid

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

@patch("src.main.send_sms")
def test_create_sms_notification(mock_send_sms, client, mock_db_session):
    # Mock db.refresh to simulate ID assignment if needed (our model uses uuid default, but for response checking)
    def mock_refresh(instance):
        instance.id = str(uuid.uuid4())
    mock_db_session.refresh.side_effect = mock_refresh

    payload = {
        "title": "Hello",
        "content": "World",
        "recipient_id": 123,
        "notification_type": "sms"
    }

    response = client.post("/api/notifications", json=payload)
    
    assert response.status_code == 200
    assert "notification_id" in response.json()
    
    # Verify send_sms was called
    mock_send_sms.assert_called_with(123, "Hello", "World")
    
    # Verify DB interactions
    mock_db_session.add.assert_called()
    mock_db_session.commit.assert_called()

@patch("src.main.send_email")
def test_create_email_notification(mock_send_email, client, mock_db_session):
    def mock_refresh(instance):
        instance.id = str(uuid.uuid4())
    mock_db_session.refresh.side_effect = mock_refresh

    payload = {
        "title": "Email Subject",
        "content": "Email Body",
        "recipient_id": 123,
        "notification_type": "email"
    }

    response = client.post("/api/notifications", json=payload)
    
    assert response.status_code == 200
    mock_send_email.assert_called_with(123, "Email Subject", "Email Body")

def test_get_notification(client, mock_db_session):
    nid = str(uuid.uuid4())
    mock_notif = Notification(id=nid, title="Test", content="Content", recipient_id=1, notification_type="sms", status="sent")
    
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_notif
    
    response = client.get(f"/api/notifications/{nid}")
    
    assert response.status_code == 200
    assert response.json()["id"] == nid
    assert response.json()["title"] == "Test"

def test_get_preferences(client, mock_db_session):
    pid = str(uuid.uuid4())
    mock_pref = Preference(id=pid, user_id=1, sms_enabled=True, email_enabled=False, in_app_enabled=True)
    
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_pref
    
    response = client.get("/api/preferences/1")
    
    assert response.status_code == 200
    data = response.json()
    assert data["sms_enabled"] is True
    assert data["email_enabled"] is False

def test_update_preferences_new(client, mock_db_session):
    # Simulate not found, creating new
    mock_db_session.query.return_value.filter.return_value.first.return_value = None
    
    payload = {
        "user_id": 1,
        "sms_enabled": True,
        "email_enabled": True,
        "in_app_enabled": True
    }
    
    response = client.patch("/api/preferences/1", json=payload)
    
    assert response.status_code == 200
    assert response.json()["message"] == "Preferences for user 1 updated"
    mock_db_session.add.assert_called()
    mock_db_session.commit.assert_called()
