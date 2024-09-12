from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_create_payment():
    response = client.post("/api/payments", json={"user_id": 1, "amount": 100.00})
    assert response.status_code == 200
    assert "payment_id" in response.json()

# Add more tests for other endpoints
