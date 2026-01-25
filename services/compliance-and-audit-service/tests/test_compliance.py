import pytest
import json
from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from datetime import datetime
from src.main import app, get_db
from src.models import AuditLog, ComplianceCheck, RiskAssessment

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
        if hasattr(obj, 'performed_at') and not obj.performed_at:
            obj.performed_at = datetime.utcnow()
        if hasattr(obj, 'generated_at') and not obj.generated_at:
            obj.generated_at = datetime.utcnow()
            
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

def test_create_audit_log(client, mock_db_session):
    payload = {
        "user_id": 1,
        "action": "login",
        "resource": "auth",
        "details": {"ip": "1.2.3.4"}
    }
    response = client.post("/api/audit", json=payload)
    
    assert response.status_code == 201
    assert response.json()["action"] == "login"
    
    added_log = mock_db_session.add.call_args[0][0]
    assert isinstance(added_log, AuditLog)
    assert json.loads(added_log.details) == payload["details"]

def test_get_audit_logs(client, mock_db_session):
    mock_log = AuditLog(
        id=1, user_id=1, action="login", resource="auth",
        details=json.dumps({"ip": "1.2.3.4"}), timestamp=datetime.utcnow()
    )
    mock_db_session.query.return_value.filter.return_value.all.return_value = [mock_log]
    
    response = client.get("/api/audit?user_id=1")
    
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["details"] == {"ip": "1.2.3.4"}

def test_perform_compliance_check(client, mock_db_session):
    payload = {"check_type": "gdpr", "details": {"scope": "all"}}
    response = client.post("/api/compliance/checks", json=payload)
    
    assert response.status_code == 201
    assert response.json()["status"] == "pass"

def test_generate_compliance_report(client):
    # This endpoint doesn't use DB, just returns a mock response
    payload = {"report_type": "audit_summary"}
    response = client.post("/api/reports/generate", json=payload)
    
    assert response.status_code == 201
    assert "download_url" in response.json()

def test_start_risk_assessment(client, mock_db_session):
    payload = {"assessment_type": "vendor_risk"}
    response = client.post("/api/risk-assessment", json=payload)
    
    assert response.status_code == 201
    assert response.json()["risk_score"] == 15
    mock_db_session.add.assert_called()

def test_get_risk_assessment_not_found(client, mock_db_session):
    mock_db_session.query.return_value.filter.return_value.first.return_value = None
    response = client.get("/api/risk-assessment/results/999")
    assert response.status_code == 404
