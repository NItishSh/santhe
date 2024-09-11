import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from pricing_service.src.main import app, get_db
from pricing_service.src.models import Price
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

def test_get_price_history(client, mock_get_db):
    app.dependency_overrides[get_db] = mock_get_db
    
    # Mock price query
    async def mock_get_price_history(product_id):
        return [
            Price(id=1, product_id=product_id, price=19.99, timestamp=datetime(2023, 1, 1)),
            Price(id=2, product_id=product_id, price=20.99, timestamp=datetime(2023, 1, 15)),
            Price(id=3, product_id=product_id, price=21.99, timestamp=datetime(2023, 2, 1))
        ]
    
    with patch('pricing_service.src.models.Price.query.filter_by', side_effect=lambda x: mock_get_price_history(x)):
        response = client.get("/api/prices/history/1?start_date=2023-01-01&end_date=2023-02-28")
        
        assert response.status_code == 200
        assert len(response.json()) == 3
        assert response.json()[0]["price"] == 19.99
        assert response.json()[-1]["price"] == 21.99
