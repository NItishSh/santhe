from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from datetime import datetime
import json
from .models import AnalyticsEvent, AnalyticsJob, Report, Dashboard
from .schemas import EventCreate, JobCreate, ReportCreate, DashboardCreate, DashboardUpdate, DashboardResponse

class AnalyticsService:
    @staticmethod
    def submit_data(db: Session, event: EventCreate) -> AnalyticsEvent:
        db_event = AnalyticsEvent(
            event_type=event.event_type,
            payload=json.dumps(event.payload) if event.payload else None
        )
        db.add(db_event)
        db.commit()
        db.refresh(db_event)
        return db_event

    @staticmethod
    def schedule_job(db: Session, job: JobCreate) -> AnalyticsJob:
        new_job = AnalyticsJob(job_type=job.job_type, status="pending")
        db.add(new_job)
        db.commit()
        db.refresh(new_job)
        return new_job

    @staticmethod
    def get_job(db: Session, job_id: int) -> Optional[AnalyticsJob]:
        return db.query(AnalyticsJob).filter(AnalyticsJob.id == job_id).first()

    @staticmethod
    def generate_report(db: Session, report: ReportCreate) -> Report:
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

    @staticmethod
    def get_report(db: Session, report_id: int) -> Optional[Report]:
        return db.query(Report).filter(Report.id == report_id).first()

    @staticmethod
    def list_dashboards(db: Session) -> List[DashboardResponse]:
        # Handle conversion from DB Text -> Dict
        dashboards = db.query(Dashboard).all()
        result = []
        for d in dashboards:
            result.append(DashboardResponse(
                id=d.id,
                name=d.name,
                configuration=json.loads(d.configuration) if d.configuration else {},
                created_at=d.created_at
            ))
        return result

    @staticmethod
    def create_dashboard(db: Session, dashboard: DashboardCreate) -> DashboardResponse:
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

    @staticmethod
    def update_dashboard(db: Session, dashboard_id: int, update: DashboardUpdate) -> Optional[DashboardResponse]:
        dashboard = db.query(Dashboard).filter(Dashboard.id == dashboard_id).first()
        if not dashboard:
            return None
        
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
