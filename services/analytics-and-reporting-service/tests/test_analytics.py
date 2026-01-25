import pytest
import json
from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from datetime import datetime
from src.main import app, get_db
from src.models import AnalyticsEvent, AnalyticsJob, Report, Dashboard


# --- Fixtures ---

@pytest.fixture
def mock_db_session():
    """Returns a mock implementation of the SQLAlchemy Session."""
    session = MagicMock()
    # Setup refresh side effect to populate IDs and defaults
    def side_effect_refresh(obj):
        obj.id = 1
        # Set timestamps if they are missing/None
        if hasattr(obj, 'timestamp') and not obj.timestamp:
            obj.timestamp = datetime.utcnow()
        if hasattr(obj, 'created_at') and not obj.created_at:
            obj.created_at = datetime.utcnow()
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

def test_submit_data(client, mock_db_session):
    payload = {
        "event_type": "page_view",
        "payload": {"url": "/home", "user": "guest"}
    }
    response = client.post("/api/analytics/data", json=payload)
    
    assert response.status_code == 201
    assert response.json()["event_type"] == "page_view"
    assert "id" in response.json()
    assert "timestamp" in response.json()
    
    # Check DB add was called with correct serialization
    added_obj = mock_db_session.add.call_args[0][0]
    assert isinstance(added_obj, AnalyticsEvent)
    assert added_obj.event_type == "page_view"
    assert json.loads(added_obj.payload) == payload["payload"]

def test_schedule_job(client, mock_db_session):
    payload = {"job_type": "daily_summary"}
    response = client.post("/api/analytics/jobs", json=payload)
    
    assert response.status_code == 201
    assert response.json()["job_type"] == "daily_summary"
    assert response.json()["status"] == "pending"
    assert "id" in response.json()
    assert "created_at" in response.json()

def test_get_job(client, mock_db_session):
    mock_job = AnalyticsJob(id=1, job_type="daily_summary", status="completed", created_at=datetime.utcnow())
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_job
    
    response = client.get("/api/analytics/jobs/1")
    
    assert response.status_code == 200
    assert response.json()["status"] == "completed"

def test_generate_report(client, mock_db_session):
    payload = {
        "report_type": "sales_report",
        "parameters": {"start_date": "2023-01-01", "end_date": "2023-01-31"}
    }
    response = client.post("/api/reports/generate", json=payload)
    
    assert response.status_code == 201
    # Mock behavior sets ID to 1 via refresh side effect
    assert response.json()["id"] == 1 
    assert response.json()["report_type"] == "sales_report"
    assert response.json()["download_url"].startswith("https://reports.santhe.com/sales_report")
    assert "generated_at" in response.json()

def test_create_dashboard_success(client, mock_db_session):
    config = {"layout": "grid", "widgets": ["chart1", "table1"]}
    payload = {
        "name": "CEO Dashboard",
        "configuration": config
    }
    
    response = client.post("/api/dashboards", json=payload)
    
    assert response.status_code == 201
    assert response.json()["name"] == "CEO Dashboard"
    assert response.json()["configuration"] == config
    assert "created_at" in response.json()
    
    added_obj = mock_db_session.add.call_args[0][0]
    assert json.loads(added_obj.configuration) == config

def test_list_dashboards(client, mock_db_session):
    # This endpoint has manual logic for JSON parsing
    config = {"theme": "dark"}
    mock_dash = Dashboard(id=1, name="Main", configuration=json.dumps(config), created_at=datetime.utcnow())
    mock_db_session.query.return_value.all.return_value = [mock_dash]
    
    response = client.get("/api/dashboards")
    
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["configuration"] == config

def test_update_dashboard(client, mock_db_session):
    old_config = {"theme": "light"}
    mock_dash = Dashboard(id=1, name="Main", configuration=json.dumps(old_config), created_at=datetime.utcnow())
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_dash
    
    new_config = {"theme": "dark"}
    payload = {"configuration": new_config}
    
    response = client.patch("/api/dashboards/1", json=payload)
    
    assert response.status_code == 200
    assert response.json()["configuration"] == new_config
    assert json.loads(mock_dash.configuration) == new_config
