from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from datetime import datetime
import json
from .models import AuditLog, ComplianceCheck, RiskAssessment
from .schemas import AuditLogCreate, CheckCreate, ReportCreate, ReportResponse, RiskAssessmentCreate

class ComplianceService:
    @staticmethod
    def create_audit_log(db: Session, log: AuditLogCreate) -> AuditLog:
        db_log = AuditLog(
            user_id=log.user_id,
            action=log.action,
            resource=log.resource,
            details=json.dumps(log.details) if log.details else None
        )
        db.add(db_log)
        db.commit()
        db.refresh(db_log)
        return db_log

    @staticmethod
    def get_audit_logs(db: Session, user_id: Optional[int] = None, action: Optional[str] = None) -> List[AuditLog]:
        query = db.query(AuditLog)
        if user_id:
            query = query.filter(AuditLog.user_id == user_id)
        if action:
            query = query.filter(AuditLog.action == action)
        return query.all()

    @staticmethod
    def get_audit_log_details(db: Session, log_id: int) -> Optional[AuditLog]:
        return db.query(AuditLog).filter(AuditLog.id == log_id).first()

    @staticmethod
    def perform_compliance_check(db: Session, check: CheckCreate) -> ComplianceCheck:
        # Mock logic as in original
        db_check = ComplianceCheck(
            check_type=check.check_type,
            status="pass", 
            details=json.dumps(check.details) if check.details else None
        )
        db.add(db_check)
        db.commit()
        db.refresh(db_check)
        return db_check

    @staticmethod
    def get_check_result(db: Session, check_id: int) -> Optional[ComplianceCheck]:
        return db.query(ComplianceCheck).filter(ComplianceCheck.id == check_id).first()

    @staticmethod
    def generate_compliance_report(report: ReportCreate) -> ReportResponse:
        # Mock logic
        return ReportResponse(
            id=f"rep_{int(datetime.utcnow().timestamp())}",
            download_url=f"https://compliance.santhe.com/reports/{report.report_type}.pdf",
            generated_at=datetime.utcnow()
        )

    @staticmethod
    def get_compliance_report(report_id: str) -> ReportResponse:
        # Mock logic
        return ReportResponse(
            id=report_id,
            download_url=f"https://compliance.santhe.com/reports/{report_id}.pdf",
            generated_at=datetime.utcnow()
        )

    @staticmethod
    def start_risk_assessment(db: Session, assessment: RiskAssessmentCreate) -> RiskAssessment:
        # Mock logic
        score = 15
        level = "Low"
        
        db_assessment = RiskAssessment(
            assessment_type=assessment.assessment_type,
            risk_score=score,
            risk_level=level,
            details=json.dumps(assessment.details) if assessment.details else None
        )
        db.add(db_assessment)
        db.commit()
        db.refresh(db_assessment)
        return db_assessment

    @staticmethod
    def get_risk_assessment(db: Session, assessment_id: int) -> Optional[RiskAssessment]:
        return db.query(RiskAssessment).filter(RiskAssessment.id == assessment_id).first()
