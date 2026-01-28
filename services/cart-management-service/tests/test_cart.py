import pytest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from src.main import app
from src.database import get_db
from src.dependencies import get_current_username

@pytest.fixture
def mock_db_session():
    """Returns a mock implementation of the SQLAlchemy Session."""
    return MagicMock()

@pytest.fixture
def client(mock_db_session):
    def override_get_db():
        try:
            yield mock_db_session
        finally:
            pass
    
    # Mock current user to avoid token logic in tests
    def override_get_current_username():
        return "testuser"

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_username] = override_get_current_username
    
    # Patch create_all
    with patch("src.main.Base.metadata.create_all"):
        with TestClient(app) as c:
            yield c
    
    app.dependency_overrides = {}

def test_get_cart_empty_creates_new(client, mock_db_session):
    # Mock behavior: No cart found initially
    mock_db_session.query.return_value.filter.return_value.first.return_value = None
    
    response = client.get("/api/cart")
    
    assert response.status_code == 200
    # Should attempt to create one
    mock_db_session.add.assert_called()
    mock_db_session.commit.assert_called()

def test_add_item_to_new_cart(client, mock_db_session):
    # Mock: No cart
    mock_db_session.query.return_value.filter.return_value.first.return_value = None
    
    payload = {"product_id": 101, "quantity": 2}
    response = client.post("/api/cart/items", json=payload)
    
    assert response.status_code == 200
    mock_db_session.add.assert_any_call() # Cart
    # We expect CartItem add too. 
    # Logic: if not cart, add cart. Then check item. No item -> add item.
    assert mock_db_session.add.call_count >= 2 

def test_update_item_quantity(client, mock_db_session):
    # Mock cart and item
    mock_cart = MagicMock()
    mock_cart.username = "testuser"
    mock_cart.id = 1
    
    mock_item = MagicMock()
    mock_item.id = 5
    mock_item.cart_id = 1
    mock_item.product_id = 101
    mock_item.quantity = 2
    
    # Complex mocking for query chains
    # 1. Get Cart
    # 2. Get Item
    
    # Simplify: we just assert response code implies flow worked if logic is simple.
    # But for meaningful test we need to mock returns carefully.
    
    # Let's skip detailed mock setup for complex queries in this snippet and rely on logic check.
    # Just asserting it calls commit is basic enough.
    
    # Mock finding cart
    mock_db_session.query.return_value.filter.return_value.first.side_effect = [mock_cart, mock_item]
    
    response = client.patch("/api/cart/items/5", json={"quantity": 5})
    
    assert response.status_code == 200
    assert mock_item.quantity == 5
    mock_db_session.commit.assert_called()

def test_remove_item(client, mock_db_session):
    mock_cart = MagicMock()
    mock_cart.id = 1
    mock_item = MagicMock()
    mock_item.id = 5
    
    mock_db_session.query.return_value.filter.return_value.first.side_effect = [mock_cart, mock_item]
    
    response = client.delete("/api/cart/items/5")
    
    assert response.status_code == 200
    mock_db_session.delete.assert_called_with(mock_item)
    mock_db_session.commit.assert_called()
