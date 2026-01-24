from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel, ConfigDict
from typing import List, Dict, Any, Optional
from datetime import datetime
from .database import get_db, engine, Base
from .models import AnalyticsEvent, AnalyticsJob, Report, Dashboard
import json

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

class EventCreate(BaseModel):
    event_type: str
    payload: Optional[Dict[str, Any]] = None

class EventResponse(BaseModel):
    id: int
    event_type: str
    timestamp: datetime
    model_config = ConfigDict(from_attributes=True)

class JobCreate(BaseModel):
    job_type: str

class JobResponse(JobCreate):
    id: int
    status: str
    created_at: datetime
    result: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class ReportCreate(BaseModel):
    report_type: str
    parameters: Optional[Dict[str, Any]] = None

class ReportResponse(BaseModel):
    id: int
    report_type: str
    generated_at: datetime
    download_url: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class DashboardCreate(BaseModel):
    name: str
    configuration: Dict[str, Any]

class DashboardUpdate(BaseModel):
    configuration: Optional[Dict[str, Any]] = None

class DashboardResponse(BaseModel):
    id: int
    name: str
    configuration: Dict[str, Any]
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


@app.post("/api/analytics/data", response_model=EventResponse, status_code=status.HTTP_201_CREATED)
def submit_data(event: EventCreate, db: Session = Depends(get_db)):
    # Mapping request to internally used "AnalyticsEvent"
    db_event = AnalyticsEvent(
        event_type=event.event_type,
        payload=json.dumps(event.payload) if event.payload else None
    )
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

@app.get("/api/analytics/status")
def get_analytics_status():
    return {"status": "operational", "timestamp": datetime.utcnow()}

@app.post("/api/analytics/jobs", response_model=JobResponse, status_code=status.HTTP_201_CREATED)
def schedule_job(job: JobCreate, db: Session = Depends(get_db)):
    new_job = AnalyticsJob(job_type=job.job_type, status="pending")
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    return new_job

@app.get("/api/analytics/jobs/{job_id}", response_model=JobResponse)
def get_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(AnalyticsJob).filter(AnalyticsJob.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@app.post("/api/reports/generate", response_model=ReportResponse, status_code=status.HTTP_201_CREATED)
def generate_report(report: ReportCreate, db: Session = Depends(get_db)):
    # Mock generation logic
    download_url = f"https://reports.santhe.com/{report.report_type}_{int(datetime.utcnow().timestamp())}.pdf"
    
    new_report = Report(
        report_type=report.report_type,
        parameters=json.dumps(report.parameters) if report.parameters else None,
        download_url=download_url
    )
    db.add(new_report)
    db.commit()
    db.refresh(new_report)
    return new_report

@app.get("/api/reports/{report_id}", response_model=ReportResponse)
def get_report(report_id: int, db: Session = Depends(get_db)):
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report

@app.get("/api/dashboards", response_model=List[DashboardResponse])
def list_dashboards(db: Session = Depends(get_db)):
    dashboards = db.query(Dashboard).all()
    # Need to verify if the response model handles string->dict conversion automatically or if we assume models.py stores text?
    # models.py stores configuration as Text. Pydantic expects Dict.
    # We should probably handle conversion in a Pydantic validator or manually map.
    # For simplicity here, let's assume manual mapping or updating model.
    # Let's do manual mapping list comp.
    result = []
    for d in dashboards:
        result.append(DashboardResponse(
            id=d.id,
            name=d.name,
            configuration=json.loads(d.configuration) if d.configuration else {},
            created_at=d.created_at
        ))
    return result

@app.post("/api/dashboards", response_model=DashboardResponse, status_code=status.HTTP_201_CREATED)
def create_dashboard(dashboard: DashboardCreate, db: Session = Depends(get_db)):
    new_dashboard = Dashboard(
        name=dashboard.name,
        configuration=json.dumps(dashboard.configuration)
    )
    db.add(new_dashboard)
    db.commit()
    db.refresh(new_dashboard)
    
    return DashboardResponse(
        id=new_dashboard.id,
        name=new_dashboard.name,
        configuration=dashboard.configuration, 
        created_at=new_dashboard.created_at
    )

@app.patch("/api/dashboards/{dashboard_id}", response_model=DashboardResponse)
def update_dashboard(dashboard_id: int, update: DashboardUpdate, db: Session = Depends(get_db)):
    dashboard = db.query(Dashboard).filter(Dashboard.id == dashboard_id).first()
    if not dashboard:
        raise HTTPException(status_code=404, detail="Dashboard not found")
    
    if update.configuration:
        dashboard.configuration = json.dumps(update.configuration)
        
    db.commit()
    db.refresh(dashboard)
    
    return DashboardResponse(
        id=dashboard.id,
        name=dashboard.name,
        configuration=json.loads(dashboard.configuration),
        created_at=dashboard.created_at
    )

@app.get("/")
def root():
    return {"message": "Welcome to the Analytics and Reporting Service"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)