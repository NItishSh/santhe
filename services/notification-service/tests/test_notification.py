import pytest
import uuid
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from src.main import app, get_db
from src.models import Notification, Preference

# --- Fixtures ---

@pytest.fixture
def mock_db_session():
    """Returns a mock implementation of the SQLAlchemy Session."""
    session = MagicMock()
    
    def side_effect_refresh(obj):
        # Notification IDs effectively generated in code (uuid), but status update?
        # Preference ID also uuid.
        # Just to be safe:
        if hasattr(obj, 'id') and not obj.id:
            obj.id = str(uuid.uuid4())
            
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

def test_create_notification_sms(client, mock_db_session):
    payload = {
        "title": "Welcome",
        "content": "Hello User",
        "recipient_id": 1,
        "notification_type": "sms"
    }
    
    # Mock external senders
    with patch("src.main.send_sms") as mock_send:
        response = client.post("/api/notifications", json=payload)
        
        assert response.status_code == 200
        assert "notification_id" in response.json()
        mock_send.assert_called_with(1, "Welcome", "Hello User")
        
        added_notification = mock_db_session.add.call_args[0][0]
        assert added_notification.status == "sent"

def test_create_notification_failure_handler(client, mock_db_session):
    payload = {
        "title": "Welcome",
        "content": "Hello User",
        "recipient_id": 1,
        "notification_type": "email"
    }
    
    # Mock external sender raising Exception
    with patch("src.main.send_email", side_effect=Exception("SMTP Error")):
        response = client.post("/api/notifications", json=payload)
        
        assert response.status_code == 200
        added_notification = mock_db_session.add.call_args[0][0]
        assert added_notification.status == "failed"

def test_get_notification(client, mock_db_session):
    valid_uuid = "123e4567-e89b-12d3-a456-426614174000"
    mock_notif = Notification(id=valid_uuid, title="Info", content="msg", recipient_id=1, notification_type="email", status="sent")
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_notif
    
    response = client.get(f"/api/notifications/{valid_uuid}")
    
    assert response.status_code == 200
    assert response.json()["title"] == "Info"

def test_update_notification_status(client, mock_db_session):
    valid_uuid = "123e4567-e89b-12d3-a456-426614174000"
    mock_notif = Notification(id=valid_uuid, status="sent")
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_notif
    
    response = client.patch(f"/api/notifications/{valid_uuid}?status=read")
    
    assert response.status_code == 200
    assert mock_notif.status == "read"

def test_get_preferences(client, mock_db_session):
    valid_uuid = "123e4567-e89b-12d3-a456-426614174001"
    mock_pref = Preference(id=valid_uuid, user_id=1, sms_enabled=True, email_enabled=False, in_app_enabled=True)
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_pref
    
    response = client.get("/api/preferences/1")
    
    assert response.status_code == 200
    assert response.json()["email_enabled"] is False

def test_update_preferences_new(client, mock_db_session):
    # Mock user doesn't exist
    mock_db_session.query.return_value.filter.return_value.first.return_value = None
    
    payload = {
        "user_id": 2,
        "sms_enabled": False,
        "email_enabled": True,
        "in_app_enabled": False
    }
    response = client.patch("/api/preferences/2", json=payload)
    
    assert response.status_code == 200
    mock_db_session.add.assert_called()
    added_pref = mock_db_session.add.call_args[0][0]
    assert added_pref.user_id == 2
    assert added_pref.sms_enabled is False

def test_update_preferences_existing(client, mock_db_session):
    # Mock existing user
    valid_uuid = "123e4567-e89b-12d3-a456-426614174001"
    mock_pref = Preference(id=valid_uuid, user_id=1, sms_enabled=True)
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_pref
    
    payload = {
        "user_id": 1,
        "sms_enabled": False,
        "email_enabled": True,
        "in_app_enabled": True
    }
    response = client.patch("/api/preferences/1", json=payload)
    
    assert response.status_code == 200
    assert mock_pref.sms_enabled is False
