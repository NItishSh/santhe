from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from .database import get_db, engine, Base
from .schemas import (
    EventCreate, EventResponse,
    JobCreate, JobResponse,
    ReportCreate, ReportResponse,
    DashboardCreate, DashboardUpdate, DashboardResponse
)
from .services import AnalyticsService

# Create tables
# Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/api/analytics/data", response_model=EventResponse, status_code=status.HTTP_201_CREATED)
def submit_data(event: EventCreate, db: Session = Depends(get_db)):
    return AnalyticsService.submit_data(db, event)

@app.get("/api/analytics/status")
def get_analytics_status():
    return {"status": "operational", "timestamp": datetime.utcnow()}

@app.post("/api/analytics/jobs", response_model=JobResponse, status_code=status.HTTP_201_CREATED)
def schedule_job(job: JobCreate, db: Session = Depends(get_db)):
    return AnalyticsService.schedule_job(db, job)

@app.get("/api/analytics/jobs/{job_id}", response_model=JobResponse)
def get_job(job_id: int, db: Session = Depends(get_db)):
    job = AnalyticsService.get_job(db, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@app.post("/api/reports/generate", response_model=ReportResponse, status_code=status.HTTP_201_CREATED)
def generate_report(report: ReportCreate, db: Session = Depends(get_db)):
    return AnalyticsService.generate_report(db, report)

@app.get("/api/reports/{report_id}", response_model=ReportResponse)
def get_report(report_id: int, db: Session = Depends(get_db)):
    report = AnalyticsService.get_report(db, report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report

@app.get("/api/dashboards", response_model=List[DashboardResponse])
def list_dashboards(db: Session = Depends(get_db)):
    return AnalyticsService.list_dashboards(db)

@app.post("/api/dashboards", response_model=DashboardResponse, status_code=status.HTTP_201_CREATED)
def create_dashboard(dashboard: DashboardCreate, db: Session = Depends(get_db)):
    return AnalyticsService.create_dashboard(db, dashboard)

@app.patch("/api/dashboards/{dashboard_id}", response_model=DashboardResponse)
def update_dashboard(dashboard_id: int, update: DashboardUpdate, db: Session = Depends(get_db)):
    dashboard_resp = AnalyticsService.update_dashboard(db, dashboard_id, update)
    if not dashboard_resp:
        raise HTTPException(status_code=404, detail="Dashboard not found")
    return dashboard_resp

@app.get("/")
def root():
    return {"message": "Welcome to the Analytics and Reporting Service"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)