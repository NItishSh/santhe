import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from pricing_service.src.main import app, get_db
from pricing_service.src.models import Price, Bid
from pricing_service.src.database import engine

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

def test_create_price(client, mock_get_db):
    app.dependency_overrides[get_db] = mock_get_db
    
    response = client.post("/api/prices", json={
        "product_id": 1,
        "price": 19.99,
        "timestamp": "2023-01-01T12:00:00"
    })
    
    assert response.status_code == 201
    assert response.json()["price"] == 19.99

def test_get_price(client, mock_get_db):
    app.dependency_overrides[get_db] = mock_get_db
    
    # Mock price query
    async def mock_get_price(price_id):
        return Price(id=price_id, product_id=1, price=19.99, timestamp=datetime(2023, 1, 1))
    
    with patch('pricing_service.src.models.Price.query.filter_by', side_effect=lambda x: mock_get_price(x)):
        response = client.get("/api/prices/1")
        
        assert response.status_code == 200
        assert response.json()["price"] == 19.99

# Add similar tests for updating, deleting prices and managing bids
