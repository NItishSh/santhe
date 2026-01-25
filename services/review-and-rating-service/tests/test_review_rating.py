import pytest
import uuid
from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from src.main import app, get_db
from src.models import Review

# --- Fixtures ---

@pytest.fixture
def mock_db_session():
    """Returns a mock implementation of the SQLAlchemy Session."""
    session = MagicMock()
    
    def side_effect_refresh(obj):
        if hasattr(obj, 'id') and not obj.id:
            obj.id = str(uuid.uuid4())
            
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
    with TestClient(app) as c:
        yield c
    app.dependency_overrides = {}

# --- Tests ---

def test_create_review(client, mock_db_session):
    payload = {
        "rating": 5,
        "content": "Excellent service",
        "reviewer_id": 1,
        "reviewed_id": 2
    }
    response = client.post("/api/reviews", json=payload)
    
    assert response.status_code == 200
    assert response.json()["rating"] == 5
    # ID is generated via uuid4, just check it exists
    assert "id" in response.json()
    mock_db_session.add.assert_called()
    mock_db_session.commit.assert_called()

def test_get_review(client, mock_db_session):
    valid_uuid = "123e4567-e89b-12d3-a456-426614174000"
    mock_review = Review(id=valid_uuid, rating=5.0, content="Good", reviewer_id=1, reviewed_id=2)
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_review
    
    response = client.get(f"/api/reviews/{valid_uuid}")
    
    assert response.status_code == 200
    assert response.json()["id"] == valid_uuid

def test_update_review(client, mock_db_session):
    valid_uuid = "123e4567-e89b-12d3-a456-426614174000"
    mock_review = Review(id=valid_uuid, rating=5.0, content="Good", reviewer_id=1, reviewed_id=2)
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_review
    
    response = client.patch(
        f"/api/reviews/{valid_uuid}", 
        params={"rating": 3, "content": "Average"}
    )
    
    assert response.status_code == 200
    assert response.json()["rating"] == 3
    assert mock_review.content == "Average"

def test_delete_review(client, mock_db_session):
    valid_uuid = "123e4567-e89b-12d3-a456-426614174000"
    mock_review = Review(id=valid_uuid)
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_review
    
    response = client.delete(f"/api/reviews/{valid_uuid}")
    
    assert response.status_code == 200
    mock_db_session.delete.assert_called_with(mock_review)

def test_get_average_rating(client, mock_db_session):
    # Mock return of tuples [(rating,), (rating,)]
    mock_db_session.query.return_value.filter.return_value.all.return_value = [(4.0,), (5.0,)]
    
    response = client.get("/api/ratings/2")
    
    assert response.status_code == 200
    assert response.json()["average_rating"] == 4.5

def test_flag_for_moderation(client, mock_db_session):
    valid_uuid = "123e4567-e89b-12d3-a456-426614174000"
    mock_review = Review(id=valid_uuid, rating=5.0, content="Rude content", reviewer_id=1, reviewed_id=2)
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_review
    
    payload = {"review_id": valid_uuid, "reason": "Harassment"}
    response = client.post("/api/moderate", json=payload)
    
    assert response.status_code == 200
    assert mock_review.content.startswith("[MODERATED]")
