import pytest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from src.main import app, get_db
from src.models import Product

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

# --- Tests ---

def test_create_product(client, mock_db_session):
    # Mock db.refresh to set ID
    def mock_refresh(instance):
        instance.id = 1

    mock_db_session.refresh.side_effect = mock_refresh

    payload = {
        "name": "Test Product",
        "description": "This is a test product",
        "price": 19.99,
        "category_id": 1
    }
    
    response = client.post("/api/products", json=payload)
    
    # Debug output if validation fails
    if response.status_code != 201:
        print(response.json())

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Product"
    assert data["id"] == 1
    
    # Verify DB interactions
    mock_db_session.add.assert_called()
    mock_db_session.commit.assert_called()
    mock_db_session.refresh.assert_called()

def test_get_product(client, mock_db_session):
    # Mock return value for query
    mock_product = Product(id=1, name="Test Product", description="Desc", price=19.99, category_id=1)
    mock_db_session.query.return_value.filter_by.return_value.first.return_value = mock_product
    
    response = client.get("/api/products/1")
    
    assert response.status_code == 200
    assert response.json()["name"] == "Test Product"

def test_get_product_not_found(client, mock_db_session):
    mock_db_session.query.return_value.filter_by.return_value.first.return_value = None
    
    response = client.get("/api/products/999")
    
    assert response.status_code == 404

def test_update_product(client, mock_db_session):
    mock_product = Product(id=1, name="Old Name", description="Desc", price=19.99, category_id=1)
    mock_db_session.query.return_value.filter_by.return_value.first.return_value = mock_product
    
    response = client.patch("/api/products/1", json={"name": "New Name"})
    
    assert response.status_code == 200
    assert response.json()["name"] == "New Name"
    # Ensure commit was called
    mock_db_session.commit.assert_called()

def test_delete_product(client, mock_db_session):
    mock_product = Product(id=1, name="Test Product", category_id=1)
    mock_db_session.query.return_value.filter_by.return_value.first.return_value = mock_product
    
    response = client.delete("/api/products/1")
    
    assert response.status_code == 200
    mock_db_session.delete.assert_called_with(mock_product)
    mock_db_session.commit.assert_called()

def test_search_products(client, mock_db_session):
    # Mock search results returning a list of products
    p1 = Product(id=1, name="Apple", description="Fruit", price=1.0, category_id=1)
    p2 = Product(id=2, name="Banana", description="Yellow Fruit", price=0.5, category_id=1)
    
    # query().filter().filter().all() chain
    # We simplify checking: we assume the filters work, here we just test that list is returned
    mock_db_session.query.return_value.filter.return_value.filter.return_value.all.return_value = [p1]
    
    # If the logic chains multiple filters, mocking exact chain is complex. 
    # Often better to just assert it returns something if mocked correctly.
    # For a unit test of the endpoint, we care that it calls the DB and returns the result.
    
    # Let's mock the final .all() result regardless of intermediate filter calls
    mock_query = mock_db_session.query.return_value
    mock_query.filter.return_value = mock_query # Chaining support
    mock_query.all.return_value = [p1, p2]

    response = client.get("/api/products/search?name=fruit")
    
    if response.status_code != 200:
        print(response.json())

    assert response.status_code == 200
    assert len(response.json()) == 2
