import pytest
from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from src.main import app, get_db
from src.models import Review
import uuid

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

def test_create_review(client, mock_db_session):
    def mock_refresh(instance):
        instance.id = str(uuid.uuid4())
    mock_db_session.refresh.side_effect = mock_refresh

    payload = {
        "rating": 5,
        "content": "Excellent service!",
        "reviewer_id": 1,
        "reviewed_id": 2
    }
    
    response = client.post("/api/reviews", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["rating"] == 5
    assert "id" in data
    
    mock_db_session.add.assert_called()
    mock_db_session.commit.assert_called()

def test_get_all_reviews(client, mock_db_session):
    mock_review = Review(id="test-uuid", rating=5, content="Great!", reviewer_id=1, reviewed_id=2)
    mock_db_session.query.return_value.all.return_value = [mock_review]
    
    response = client.get("/api/reviews")
    assert response.status_code == 200
    assert len(response.json()) == 1

def test_get_review(client, mock_db_session):
    mock_review = Review(id="test-uuid", rating=5, content="Great!", reviewer_id=1, reviewed_id=2)
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_review
    
    response = client.get("/api/reviews/test-uuid")
    assert response.status_code == 200
    assert response.json()["id"] == "test-uuid"

def test_update_review(client, mock_db_session):
    mock_review = Review(id="test-uuid", rating=5, content="Great!", reviewer_id=1, reviewed_id=2)
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_review
    
    response = client.patch("/api/reviews/test-uuid?rating=4&content=Good")
    assert response.status_code == 200
    assert response.json()["rating"] == 4
    
    assert mock_review.rating == 4

def test_delete_review(client, mock_db_session):
    mock_review = Review(id="test-uuid", rating=5, content="Great!", reviewer_id=1, reviewed_id=2)
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_review
    
    response = client.delete("/api/reviews/test-uuid")
    assert response.status_code == 200
    assert response.json()["message"] == "Review deleted"

def test_get_average_rating(client, mock_db_session):
    # Mocking list of tuples (rating,)
    mock_db_session.query.return_value.filter.return_value.all.return_value = [(5,), (4,)]
    
    response = client.get("/api/ratings/2")
    assert response.status_code == 200
    assert response.json()["average_rating"] == 4.5

def test_rate_user(client, mock_db_session):
    def mock_refresh(instance):
        instance.id = str(uuid.uuid4())
    mock_db_session.refresh.side_effect = mock_refresh
    
    payload = {"rating": 5, "rated_user_id": 1}
    response = client.post("/api/ratings", json=payload)
    
    assert response.status_code == 200
    assert "review_id" in response.json()

def test_flag_for_moderation(client, mock_db_session):
    mock_review = Review(id="test-uuid", rating=5, content="Bad word", reviewer_id=1, reviewed_id=2)
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_review
    
    payload = {"review_id": "test-uuid", "reason": "Profanity"}
    response = client.post("/api/moderate", json=payload)
    
    assert response.status_code == 200
    assert response.json()["message"] == "Review flagged for moderation"
    assert mock_review.content.startswith("[MODERATED]")

def test_get_moderated_reviews(client, mock_db_session):
    mock_review = Review(id="test-uuid", rating=5, content="[MODERATED] Bad word", reviewer_id=1, reviewed_id=2)
    mock_db_session.query.return_value.filter.return_value.all.return_value = [mock_review]
    
    response = client.get("/api/moderated-reviews")
    assert response.status_code == 200
    assert len(response.json()) == 1
