import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from product_catalog_service.src.main import app, get_db
from product_catalog_service.src.models import Product, Category
from product_catalog_service.src.database import engine

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

def test_create_product(client, mock_get_db):
    app.dependency_overrides[get_db] = mock_get_db
    
    response = client.post("/api/products", json={
        "name": "Test Product",
        "description": "This is a test product",
        "price": 19.99,
        "category_id": 1
    })
    
    assert response.status_code == 201
    assert response.json()["name"] == "Test Product"

def test_get_product(client, mock_get_db):
    app.dependency_overrides[get_db] = mock_get_db
    
    # Mock product query
    async def mock_get_product(product_id):
        return Product(id=product_id, name="Test Product", description="Description", price=19.99)
    
    with patch('product_catalog_service.src.models.Product.query.filter_by', side_effect=lambda x: mock_get_product(x)):
        response = client.get("/api/products/1")
        
        assert response.status_code == 200
        assert response.json()["name"] == "Test Product"

def test_update_product(client, mock_get_db):
    app.dependency_overrides[get_db] = mock_get_db
    
    # Mock product query
    async def mock_get_product(product_id):
        return Product(id=product_id, name="Old Name", description="Description", price=19.99)
    
    with patch('product_catalog_service.src.models.Product.query.filter_by', side_effect=lambda x: mock_get_product(x)):
        response = client.patch("/api/products/1", json={
            "name": "New Name"
        })
        
        assert response.status_code == 200
        assert response.json()["name"] == "New Name"

def test_delete_product(client, mock_get_db):
    app.dependency_overrides[get_db] = mock_get_db
    
    # Mock product query
    async def mock_get_product(product_id):
        return Product(id=product_id, name="Test Product", description="Description", price=19.99)
    
    with patch('product_catalog_service.src.models.Product.query.filter_by', side_effect=lambda x: mock_get_product(x)):
        response = client.delete("/api/products/1")
        
        assert response.status_code == 200
        assert response.json()["message"] == "Product 1 deleted successfully"

# Add similar tests for categories
def test_search_products(client, mock_get_db):
    app.dependency_overrides[get_db] = mock_get_db
    
    # Mock product query
    async def mock_search_products(name=None, description=None, category_id=None):
        products = [
            Product(id=1, name="Test Product", description="Description", price=19.99),
            Product(id=2, name="Another Product", description="Different Description", price=29.99)
        ]
        if name:
            products = [p for p in products if name.lower() in p.name.lower()]
        if description:
            products = [p for p in products if description.lower() in p.description.lower()]
        if category_id:
            products = [p for p in products if p.category_id == category_id]
        return products
    
    with patch('product_catalog_service.src.models.Product.query', side_effect=lambda *args, **kwargs: mock_search_products(*args, **kwargs)):
        response = client.get("/api/products/search?name=test&description=desc")
        
        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()[0]["name"] == "Test Product"

def test_filter_products(client, mock_get_db):
    app.dependency_overrides[get_db] = mock_get_db
    
    # Mock product query
    async def mock_filter_products(min_price=None, max_price=None, category_id=None):
        products = [
            Product(id=1, name="Test Product", description="Description", price=19.99),
            Product(id=2, name="Another Product", description="Different Description", price=29.99)
        ]
        if min_price:
            products = [p for p in products if p.price >= min_price]
        if max_price:
            products = [p for p in products if p.price <= max_price]
        if category_id:
            products = [p for p in products if p.category_id == category_id]
        return products
    
    with patch('product_catalog_service.src.models.Product.query', side_effect=lambda *args, **kwargs: mock_filter_products(*args, **kwargs)):
        response = client.get("/api/products/filter?min_price=20&max_price=30")
        
        assert response.status_code == 200
        assert len(response.json()) == 2
        assert response.json()[0]["price"] == 19.99
        assert response.json()[1]["price"] == 29.99
