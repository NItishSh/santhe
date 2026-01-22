import pytest
from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from src.main import app, get_db
from src.models import Price

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

def test_create_price(client, mock_db_session):
    def mock_refresh(instance):
        instance.id = 1
        # No timestamp to set here as it's passed in
    mock_db_session.refresh.side_effect = mock_refresh

    payload = {
        "product_id": 1,
        "price": 19.99,
        "timestamp": "2023-01-01T12:00:00"
    }
    
    response = client.post("/api/prices", json=payload)
    
    assert response.status_code == 201
    data = response.json()
    assert data["product_id"] == 1
    assert data["price"] == 19.99
    
    mock_db_session.add.assert_called()
    mock_db_session.commit.assert_called()

def test_get_price(client, mock_db_session):
    mock_price = Price(id=1, product_id=1, price=19.99, timestamp="2023-01-01T12:00:00")
    
    # Mocking query.filter.first
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_price
    
    response = client.get("/api/prices/1")
    
    assert response.status_code == 200
    data = response.json()
    assert data["price"] == 19.99

def test_update_price(client, mock_db_session):
    mock_price = Price(id=1, product_id=1, price=19.99, timestamp="2023-01-01T12:00:00")
    
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_price
    
    payload = {"price": 25.00}
    response = client.patch("/api/prices/1", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["price"] == 25.00
    
    assert mock_price.price == 25.00
    mock_db_session.commit.assert_called()

def test_get_price_history(client, mock_db_session):
    mock_price = Price(id=1, product_id=1, price=19.99, timestamp="2023-01-01T12:00:00")
    
    # Mocking query.filter.filter.order_by.all
    # This chain is long: query -> filter(product) -> [filter(date)] -> order_by -> all
    
    mock_query = mock_db_session.query.return_value
    mock_query.filter.return_value = mock_query # For product_id and dates
    mock_query.order_by.return_value.all.return_value = [mock_price]
    
    response = client.get("/api/prices/history/1")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["price"] == 19.99
