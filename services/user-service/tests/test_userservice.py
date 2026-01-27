import pytest
from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from src.main import app, get_db, get_current_user


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

# --- Tests for /register ---

def test_register_user_success(client, mock_db_session):
    # Mock behavior: User not found (so we can register a new one)
    # db.query(User).filter(...).first() -> None
    mock_query = mock_db_session.query.return_value
    mock_query.filter.return_value.first.return_value = None
    mock_query.filter_by.return_value.first.return_value = None

    payload = {
        "username": "newuser",
        "email": "new@example.com",
        "password": "securepassword",
        "role": "farmer"
    }
    
    response = client.post("/api/users/register", json=payload)
    
    assert response.status_code == 201
    resp_json = response.json()
    assert resp_json["message"] == "User created successfully"
    assert "user_id" in resp_json 
    
    # Verify DB interactions
    mock_db_session.add.assert_called()
    mock_db_session.commit.assert_called()
    mock_db_session.refresh.assert_called()

def test_read_users_me_success(client, mock_db_session):
    # Mock user object
    mock_user = MagicMock()
    mock_user.id = 1
    mock_user.username = "testuser"
    mock_user.email = "test@example.com"
    mock_user.role = "farmer"
    mock_user.first_name = None
    mock_user.last_name = None
    mock_user.phone_number = None
    mock_user.address = None
    mock_user.date_of_birth = None
    mock_user.payment_method_token = None

    # Override get_current_user dependency
    async def mock_get_current_user_dep():
        return mock_user
    
    app.dependency_overrides[get_current_user] = mock_get_current_user_dep
    
    # Header not strictly needed if dependency is overridden, 
    # but good practice to keep it consistent with real requests logic if we verified token.
    # Here we skip auth logic entirely via override.
    response = client.get("/api/users/me")
    
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "username": "testuser",
        "email": "test@example.com",
        "role": "farmer",
        "first_name": None,
        "last_name": None,
        "phone_number": None,
        "address": None,
        "date_of_birth": None,
        "payment_method_token": None
    }
    
    # cleanup
    del app.dependency_overrides[get_current_user]
