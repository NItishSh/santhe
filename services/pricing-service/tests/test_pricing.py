import pytest
from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from datetime import datetime
from src.main import app
from src.routes import get_db
from src.models import Price, Bid

# --- Fixtures ---

@pytest.fixture
def mock_db_session():
    """Returns a mock implementation of the SQLAlchemy Session."""
    session = MagicMock()
    
    def side_effect_refresh(obj):
        if hasattr(obj, 'id') and not obj.id:
            obj.id = 1
        if hasattr(obj, 'timestamp') and not obj.timestamp:
            obj.timestamp = datetime.utcnow()
            
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
    
    # Patch create_all
    from unittest.mock import patch
    with patch("src.main.Base.metadata.create_all"):
        with TestClient(app) as c:
            yield c
            
    app.dependency_overrides = {}

# --- Tests for Prices ---

def test_create_price(client, mock_db_session):
    payload = {
        "product_id": 1,
        "price": 100.0,
        "timestamp": datetime.utcnow().isoformat()
    }
    response = client.post("/api/prices", json=payload)
    
    assert response.status_code == 201
    assert response.json()["price"] == 100.0
    mock_db_session.add.assert_called()
    mock_db_session.commit.assert_called()

def test_get_price(client, mock_db_session):
    mock_price = Price(
        id=1, product_id=1, price=100.0, 
        timestamp=datetime.utcnow()
    )
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_price
    
    response = client.get("/api/prices/1")
    
    assert response.status_code == 200
    assert response.json()["id"] == 1

def test_get_price_history(client, mock_db_session):
    mock_price = Price(
        id=1, product_id=1, price=100.0, 
        timestamp=datetime.utcnow()
    )
    # Mocking order_by().all()
    mock_query = mock_db_session.query.return_value
    mock_query.filter.return_value = mock_query
    mock_query.order_by.return_value.all.return_value = [mock_price]
    
    response = client.get("/api/prices/history/1")
    
    assert response.status_code == 200
    assert len(response.json()) == 1

# --- Tests for Bids ---

def test_create_bid(client, mock_db_session):
    payload = {
        "product_id": 1,
        "bid_amount": 90.0,
        "bidder_id": 2
    }
    response = client.post("/api/bids", json=payload)
    
    assert response.status_code == 201
    assert response.json()["bid_amount"] == 90.0
    # timestamp is auto-generated in endpoint, assert exists
    assert "timestamp" in response.json()

def test_get_bid_success(client, mock_db_session):
    mock_bid = Bid(id=1, product_id=1, bid_amount=90.0, bidder_id=2, timestamp=datetime.utcnow())
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_bid
    
    response = client.get("/api/bids/1")
    
    assert response.status_code == 200
    assert response.json()["bid_amount"] == 90.0

def test_update_bid(client, mock_db_session):
    mock_bid = Bid(id=1, product_id=1, bid_amount=90.0, bidder_id=2, timestamp=datetime.utcnow())
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_bid
    
    payload = {"bid_amount": 95.0}
    response = client.patch("/api/bids/1", json=payload)
    
    assert response.status_code == 200
    assert response.json()["bid_amount"] == 95.0
    assert mock_bid.bid_amount == 95.0

def test_cancel_bid(client, mock_db_session):
    mock_bid = Bid(id=1)
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_bid
    
    response = client.delete("/api/bids/1")
    
    assert response.status_code == 200
    mock_db_session.delete.assert_called_with(mock_bid)
