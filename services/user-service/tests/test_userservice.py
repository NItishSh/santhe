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
    
    response = client.post("/register", json=payload)
    
    assert response.status_code == 201
    assert response.json() == {"message": "User created successfully"}
    
    # Verify DB interactions
    mock_db_session.add.assert_called()
    mock_db_session.commit.assert_called()
    mock_db_session.refresh.assert_called()

def test_register_user_already_exists(client, mock_db_session):
    # Mock behavior: User already exists
    mock_user = User(id=1, username="existing", email="old@example.com")
    mock_db_session.query.return_value.filter_by.return_value.first.return_value = mock_user

    payload = {
        "username": "existing",
        "email": "old@example.com",
        "password": "securepassword",
        "role": "farmer"
    }

    response = client.post("/register", json=payload)

    assert response.status_code == 400
    assert response.json()["detail"] == "Username already exists"
    
    # Ensure add/commit were NOT called
    mock_db_session.add.assert_not_called()
    mock_db_session.commit.assert_not_called()

# --- Tests for /login ---

def test_login_success(client, mock_db_session):
    # Mock behavior: User found and password matches
    mock_user = MagicMock()
    mock_user.username = "testuser"
    mock_user.verify_password.return_value = True
    
    mock_db_session.query.return_value.filter_by.return_value.first.return_value = mock_user

    # Mock create_access_token to return a fixed token
    with patch("src.main.create_access_token", return_value="fake_token"):
        response = client.post("/login", params={"username": "testuser", "password": "correct"})

    assert response.status_code == 200
    data = response.json()
    assert data["access_token"] == "fake_token"
    assert data["token_type"] == "bearer"

def test_login_invalid_password(client, mock_db_session):
    # Mock behavior: User found but password incorrect
    mock_user = MagicMock()
    mock_user.username = "testuser"
    mock_user.verify_password.return_value = False
    
    mock_db_session.query.return_value.filter_by.return_value.first.return_value = mock_user

    response = client.post("/login", params={"username": "testuser", "password": "wrong"})

    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"

def test_login_user_not_found(client, mock_db_session):
    # Mock behavior: User not found
    mock_db_session.query.return_value.filter_by.return_value.first.return_value = None

    response = client.post("/login", params={"username": "unknown", "password": "any"})

    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"

# --- Tests for /users/me ---

def test_read_users_me_success(client):
    # Mock verify_token dependency
    # NOTE: Since /users/me uses Depends(verify_token), we can override that dependency directly 
    # OR replicate the token logic. Overriding is cleaner for unit tests.
    
    from src.services import verify_token
    # But wait, services.verify_token is imported in main.py as dependency. 
    # We can use app.dependency_overrides for verify_token too.
    
    async def mock_verify_token_dep(token: str = None):
        return {"sub": "testuser"}
    
    from src.main import verify_token as main_verify_token
    app.dependency_overrides[main_verify_token] = mock_verify_token_dep
    
    # We also need to be careful if the original verify_token depends on other things, 
    # but here it's just a function.
    
    response = client.get("/users/me", headers={"Authorization": "Bearer any_token"})
    
    assert response.status_code == 200
    assert response.json() == {"username": "testuser"}
    
    # cleanup
    del app.dependency_overrides[main_verify_token]

