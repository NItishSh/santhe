import pytest
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from user_service.src.main import app, get_db
from user_service.src.models import User
from user_service.src.services import create_access_token, verify_token
from user_service.src.database import engine

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

@pytest.fixture(scope="function")
async def session():
    async with engine.begin() as conn:
        yield conn

@pytest.fixture(scope="function")
async def mock_get_db(session):
    async def mock_db():
        return session
    return mock_db

@pytest.fixture(scope="function")
async def mock_verify_token():
    async def mock_verify(token):
        if token == "valid_token":
            return {"sub": "test_user"}
        return None
    return mock_verify

def test_create_access_token():
    payload = {"sub": "test_user"}
    token = create_access_token(payload)
    assert token is not None

@pytest.mark.asyncio
async def test_verify_token(mock_verify_token):
    async def mock_verify(token):
        if token == "valid_token":
            return {"sub": "test_user"}
        return None

    with patch('user_service.src.services.verify_token', side_effect=mock_verify):
        result = await verify_token("valid_token")
        assert result == {"sub": "test_user"}

@pytest.mark.asyncio
async def test_register_user(client, mock_get_db):
    app.dependency_overrides[get_db] = mock_get_db
    
    response = await client.post("/register", json={
        "username": "test_user",
        "email": "test@example.com",
        "password": "test_password",
        "role": "farmer"
    })
    
    assert response.status_code == 201
    assert response.json()["message"] == "User created successfully"

@pytest.mark.asyncio
async def test_register_existing_user(client, mock_get_db):
    app.dependency_overrides[get_db] = mock_get_db
    
    # Mock existing user
    async def mock_get_user(username):
        return User(id=1, username=username, email="test@example.com", hashed_password="hashed_password")
    
    with patch('user_service.src.models.User.query.filter_by', side_effect=lambda x: mock_get_user(x)):
        response = await client.post("/register", json={
            "username": "test_user",
            "email": "test@example.com",
            "password": "test_password",
            "role": "farmer"
        })
        
        assert response.status_code == 400
        assert response.json()["detail"] == "Username already exists"

@pytest.mark.asyncio
async def test_login(client, mock_get_db):
    app.dependency_overrides[get_db] = mock_get_db
    
    # Mock user query
    async def mock_get_user(username):
        return User(id=1, username=username, email="test@example.com", hashed_password="$2b$12$hashed_password")
    
    with patch('user_service.src.models.User.query.filter_by', side_effect=lambda x: mock_get_user(x)):
        response = await client.post("/login", data={"username": "test_user", "password": "test_password"})
        
        assert response.status_code == 200
        assert "access_token" in response.json()
        assert response.json()["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_login_invalid_credentials(client, mock_get_db):
    app.dependency_overrides[get_db] = mock_get_db
    
    # Mock user query
    async def mock_get_user(username):
        return None
    
    with patch('user_service.src.models.User.query.filter_by', side_effect=lambda x: mock_get_user(x)):
        response = await client.post("/login", data={"username": "invalid_user", "password": "wrong_password"})
        
        assert response.status_code == 401
        assert response.json()["detail"] == "Incorrect username or password"

@pytest.mark.asyncio
async def test_read_users_me(client, mock_verify_token):
    async def mock_verify(token):
        if token == "valid_token":
            return {"sub": "test_user"}
        return None

    with patch('user_service.src.services.verify_token', side_effect=mock_verify):
        response = await client.get("/users/me", headers={"Authorization": "Bearer valid_token"})
        
        assert response.status_code == 200
        assert response.json()["username"] == "test_user"

@pytest.mark.asyncio
async def test_read_users_me_invalid_token(client, mock_verify_token):
    async def mock_verify(token):
        return None

    with patch('user_service.src.services.verify_token', side_effect=mock_verify):
        response = await client.get("/users/me", headers={"Authorization": "Bearer invalid_token"})
        
        assert response.status_code == 401
