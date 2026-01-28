import pytest
from unittest.mock import MagicMock, patch, PropertyMock
from fastapi.testclient import TestClient
from datetime import datetime
from src.main import app
from src.database import get_db
from src.dependencies import get_current_username
from src.models import Cart, CartItem


def create_mock_cart(username="testuser", cart_id=1, items=None):
    """Create a mock cart with proper attributes for Pydantic validation."""
    cart = MagicMock(spec=Cart)
    cart.id = cart_id
    cart.username = username
    cart.created_at = datetime.utcnow()
    cart.updated_at = datetime.utcnow()
    cart.items = items or []
    return cart


def create_mock_cart_item(item_id=1, cart_id=1, product_id=101, quantity=1):
    """Create a mock cart item with proper attributes."""
    item = MagicMock(spec=CartItem)
    item.id = item_id
    item.cart_id = cart_id
    item.product_id = product_id
    item.quantity = quantity
    return item


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
    """Test that accessing cart creates one if it doesn't exist."""
    # First call returns None (no cart), after add/commit/refresh, return new cart
    new_cart = create_mock_cart()
    
    mock_db_session.query.return_value.filter.return_value.first.return_value = None
    mock_db_session.refresh.side_effect = lambda cart: setattr(cart, 'items', [])
    
    # After commit, the cart should be returned - configure add to capture and refresh to set
    def mock_refresh(obj):
        obj.id = 1
        obj.items = []
        obj.created_at = datetime.utcnow()
        obj.updated_at = datetime.utcnow()
    
    mock_db_session.refresh.side_effect = mock_refresh
    
    response = client.get("/api/cart")
    
    assert response.status_code == 200
    mock_db_session.add.assert_called()
    mock_db_session.commit.assert_called()


def test_add_item_to_new_cart(client, mock_db_session):
    """Test adding item creates cart if needed."""
    mock_db_session.query.return_value.filter.return_value.first.return_value = None
    
    def mock_refresh(obj):
        obj.id = 1
        obj.items = []
        obj.created_at = datetime.utcnow()
        obj.updated_at = datetime.utcnow()
    
    mock_db_session.refresh.side_effect = mock_refresh
    
    payload = {"product_id": 101, "quantity": 2}
    response = client.post("/api/cart/items", json=payload)
    
    assert response.status_code == 200
    assert mock_db_session.add.call_count >= 1


def test_update_item_quantity(client, mock_db_session):
    """Test updating item quantity."""
    mock_cart = create_mock_cart()
    mock_item = create_mock_cart_item(item_id=5, quantity=2)
    mock_cart.items = [mock_item]
    
    # First filter call returns cart, second returns item
    mock_db_session.query.return_value.filter.return_value.first.side_effect = [mock_cart, mock_item]
    
    def mock_refresh(obj):
        pass  # Keep existing attributes
    
    mock_db_session.refresh.side_effect = mock_refresh
    
    response = client.patch("/api/cart/items/5", json={"quantity": 5})
    
    assert response.status_code == 200
    assert mock_item.quantity == 5
    mock_db_session.commit.assert_called()


def test_remove_item(client, mock_db_session):
    """Test removing item from cart."""
    mock_item = create_mock_cart_item(item_id=5)
    mock_cart = create_mock_cart(items=[mock_item])
    
    mock_db_session.query.return_value.filter.return_value.first.side_effect = [mock_cart, mock_item]
    
    def mock_refresh(obj):
        obj.items = []  # Item removed
    
    mock_db_session.refresh.side_effect = mock_refresh
    
    response = client.delete("/api/cart/items/5")
    
    assert response.status_code == 200
    mock_db_session.delete.assert_called_with(mock_item)
    mock_db_session.commit.assert_called()
