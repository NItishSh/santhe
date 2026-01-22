import pytest
from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from src.main import app, get_db
from src.models import AuditLog

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

def test_create_audit_log(client, mock_db_session):
    def mock_refresh(instance):
        instance.id = 1
        instance.timestamp = "2023-01-01T00:00:00"
    mock_db_session.refresh.side_effect = mock_refresh

    payload = {
        "user_id": 1,
        "action": "login",
        "resource": "auth",
        "details": {"ip": "127.0.0.1"}
    }
    
    response = client.post("/api/audit", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["action"] == "login"
    assert data["id"] == 1
    
    mock_db_session.add.assert_called()
    mock_db_session.commit.assert_called()

def test_get_audit_logs(client, mock_db_session):
    mock_log = AuditLog(id=1, user_id=1, action="login", resource="auth", timestamp="2023-01-01T00:00:00")
    
    # Mock filtering logic is complex with pure mocks, usually we just mock the return of .all()
    # If the endpoint chains calls (query.filter.filter.all), we need to mock the chain.
    
    # Mock the query object itself to return self on filter calls
    mock_query = mock_db_session.query.return_value
    mock_query.filter.return_value = mock_query # Chaining
    mock_query.all.return_value = [mock_log]
    
    response = client.get("/api/audit?user_id=1")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["action"] == "login"
