import pytest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from src.main import app, get_db
from src.models import User

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
    # db.query(User).filter_by(username=...).first() -> None
    mock_db_session.query.return_value.filter_by.return_value.first.return_value = None

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
    # Since new_user.id is a Mock int (likely), it might be None or a specific mock value.
    # We just check the key exists.
    
    # Verify DB interactions
    mock_db_session.add.assert_called()
    mock_db_session.commit.assert_called()
    mock_db_session.refresh.assert_called()

# ... (middle tests skipped) ...

def test_read_users_me_success(client, mock_db_session):
    # Mock verify_token dependency
    # NOTE: Since /users/me uses Depends(verify_token), we can override that dependency directly 
    # OR replicate the token logic. Overriding is cleaner for unit tests.
    
    from src.services import verify_token
    async def mock_verify_token_dep(token: str = None):
        return {"sub": "testuser"}
    
    from src.main import verify_token as main_verify_token
    app.dependency_overrides[main_verify_token] = mock_verify_token_dep
    
    # Mock DB return
    mock_user = MagicMock()
    mock_user.id = 1
    mock_user.username = "testuser"
    mock_user.email = "test@example.com"
    mock_user.role = "farmer"
    
    mock_db_session.query.return_value.filter_by.return_value.first.return_value = mock_user

    response = client.get("/api/users/me", headers={"Authorization": "Bearer any_token"})
    
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "username": "testuser",
        "email": "test@example.com",
        "role": "farmer"
    }
    
    # cleanup
    del app.dependency_overrides[main_verify_token]

