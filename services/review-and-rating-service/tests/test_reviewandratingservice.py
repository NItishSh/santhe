# tests/test_review.py

import pytest
from fastapi.testclient import TestClient
from src.main import app

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

def test_create_review(client):
    review_data = {
        "rating": 5,
        "content": "Excellent service!",
        "reviewer_id": 1,
        "reviewed_id": 2
    }
    response = client.post("/api/reviews", json=review_data)
    assert response.status_code == 200
    assert "review_id" in response.json()

def test_get_all_reviews(client):
    client.post("/api/reviews", json={"rating": 5, "content": "Great!", "reviewer_id": 1, "reviewed_id": 2})
    response = client.get("/api/reviews")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0

def test_get_review(client):
    review_data = {"rating": 5, "content": "Excellent!", "reviewer_id": 1, "reviewed_id": 2}
    create_response = client.post("/api/reviews", json=review_data)
    review_id = create_response.json()["review_id"]
    
    response = client.get(f"/api/reviews/{review_id}")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert response.json()["id"] == review_id

def test_update_review(client):
    review_data = {"rating": 5, "content": "Excellent!", "reviewer_id": 1, "reviewed_id": 2}
    create_response = client.post("/api/reviews", json=review_data)
    review_id = create_response.json()["review_id"]
    
    update_response = client.patch(f"/api/reviews/{review_id}", json={"rating": 4, "content": "Very good!"})
    assert update_response.status_code == 200
    assert update_response.json()["rating"] == 4

def test_delete_review(client):
    review_data = {"rating": 5, "content": "Excellent!", "reviewer_id": 1, "reviewed_id": 2}
    create_response = client.post("/api/reviews", json=review_data)
    review_id = create_response.json()["review_id"]
    
    delete_response = client.delete(f"/api/reviews/{review_id}")
    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "Review deleted"

def test_get_average_rating(client):
    client.post("/api/reviews", json={"rating": 5, "content": "Great!", "reviewer_id": 1, "reviewed_id": 2})
    client.post("/api/reviews", json={"rating": 4, "content": "Very good!", "reviewer_id": 3, "reviewed_id": 2})
    
    response = client.get("/api/ratings/2")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert response.json()["average_rating"] == 4.5

def test_rate_user(client):
    rating_data = {"rating": 5, "rated_user_id": 1}
    response = client.post("/api/ratings", json=rating_data)
    assert response.status_code == 200
    assert "review_id" in response.json()

def test_flag_for_moderation(client):
    review_data = {"rating": 5, "content": "Excellent!", "reviewer_id": 1, "reviewed_id": 2}
    create_response = client.post("/api/reviews", json=review_data)
    review_id = create_response.json()["review_id"]
    
    moderation_response = client.post("/api/moderate", json={"review_id": review_id, "reason": "Test moderation"})
    assert moderation_response.status_code == 200
    assert moderation_response.json()["message"] == "Review flagged for moderation"

def test_get_moderated_reviews(client):
    review_data = {"rating": 5, "content": "Excellent!", "reviewer_id": 1, "reviewed_id": 2}
    create_response = client.post("/api/reviews", json=review_data)
    review_id = create_response.json()["review_id"]
    
    moderation_response = client.post("/api/moderate", json={"review_id": review_id, "reason": "Test moderation"})
    
    moderated_response = client.get("/api/moderated-reviews")
    assert moderated_response.status_code == 200
    assert isinstance(moderated_response.json(), list)
    assert len(moderated_response.json()) > 0
