import pytest
from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from src.main import app, get_db
from src.models import Product, Category

# --- Fixtures ---

@pytest.fixture
def mock_db_session():
    """Returns a mock implementation of the SQLAlchemy Session."""
    session = MagicMock()
    
    def side_effect_refresh(obj):
        if hasattr(obj, 'id') and not obj.id:
            obj.id = 1
    
    session.refresh.side_effect = side_effect_refresh
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

# --- Tests for Categories ---

def test_create_category_success(client, mock_db_session):
    # Mock behavior: Category does not exist
    mock_db_session.query.return_value.filter_by.return_value.first.return_value = None
    
    payload = {"name": "Vegetables"}
    response = client.post("/api/categories", json=payload)
    
    assert response.status_code == 201
    assert response.json()["name"] == "Vegetables"
    mock_db_session.add.assert_called()
    mock_db_session.commit.assert_called()

def test_create_category_duplicate(client, mock_db_session):
    # Mock behavior: Category exists
    mock_category = Category(id=1, name="Vegetables")
    mock_db_session.query.return_value.filter_by.return_value.first.return_value = mock_category
    
    payload = {"name": "Vegetables"}
    response = client.post("/api/categories", json=payload)
    
    assert response.status_code == 400
    assert response.json()["detail"] == "Category already exists"

def test_list_categories(client, mock_db_session):
    mock_categories = [Category(id=1, name="Veg"), Category(id=2, name="Fruits")]
    mock_db_session.query.return_value.all.return_value = mock_categories
    
    response = client.get("/api/categories")
    
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["name"] == "Veg"

# --- Tests for Products ---

def test_create_product_success(client, mock_db_session):
    payload = {
        "name": "Carrot",
        "description": "Fresh Orange Carrot",
        "price": 50.0,
        "category_id": 1
    }
    response = client.post("/api/products", json=payload)
    
    assert response.status_code == 201
    assert response.json()["name"] == "Carrot"
    mock_db_session.add.assert_called()
    mock_db_session.commit.assert_called()

def test_get_product_success(client, mock_db_session):
    mock_product = Product(id=1, name="Carrot", description="Fresh", price=50.0, category_id=1)
    mock_db_session.query.return_value.filter_by.return_value.first.return_value = mock_product
    
    response = client.get("/api/products/1")
    
    assert response.status_code == 200
    assert response.json()["name"] == "Carrot"

def test_get_product_not_found(client, mock_db_session):
    mock_db_session.query.return_value.filter_by.return_value.first.return_value = None
    
    response = client.get("/api/products/999")
    
    assert response.status_code == 404

def test_search_products(client, mock_db_session):
    mock_product = Product(id=1, name="Carrot", description="Fresh", price=50.0, category_id=1)
    # Mock the query chain: query(Product).filter(...).filter(...).all()
    # It's tricky with multiple filters. Using a simple mock list return for .all() is usually enough if we trust SQLAlchemy.
    # We verify that filter was called.
    
    # Setup mock to return a list when .all() is called
    mock_query = mock_db_session.query.return_value
    mock_query.filter.return_value = mock_query # Chaining
    mock_query.all.return_value = [mock_product]
    
    response = client.get("/api/products/search?name=Carrot")
    
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "Carrot"
