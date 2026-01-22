import pytest
from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from src.main import app, get_db
from src.models import AnalyticsEvent

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

def test_create_event(client, mock_db_session):
    def mock_refresh(instance):
        instance.id = 1
        instance.timestamp = "2023-01-01T00:00:00"
    mock_db_session.refresh.side_effect = mock_refresh

    payload = {
        "event_type": "user_signup",
        "payload": {"source": "web"}
    }
    
    response = client.post("/api/events", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["event_type"] == "user_signup"
    assert "id" in data
    
    mock_db_session.add.assert_called()
    mock_db_session.commit.assert_called()

def test_get_daily_report(client, mock_db_session):
    # Mock aggregation query result
    # SQLAlchemy query results are typically keyed tuples or objects
    mock_db_session.query.return_value.group_by.return_value.all.return_value = [
        ("user_signup", 10),
        ("order_created", 5)
    ]
    
    response = client.get("/api/reports/daily")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["event_type"] == "user_signup"
    assert data[0]["count"] == 10
