from fastapi import FastAPI, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from .database import get_db, engine, Base
from .schemas import (
    AuditLogCreate, AuditLogResponse,
    CheckCreate, CheckResponse,
    ReportCreate, ReportResponse,
    RiskAssessmentCreate, RiskAssessmentResponse
)
from .services import ComplianceService

# Create tables
# Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/api/audit", response_model=AuditLogResponse, status_code=status.HTTP_201_CREATED)
def create_audit_log(log: AuditLogCreate, db: Session = Depends(get_db)):
    return ComplianceService.create_audit_log(db, log)

@app.get("/api/audit", response_model=List[AuditLogResponse])
def get_audit_logs(
    user_id: Optional[int] = Query(None),
    action: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    return ComplianceService.get_audit_logs(db, user_id, action)

@app.get("/api/logs/{log_id}", response_model=AuditLogResponse)
def get_audit_log_details(log_id: int, db: Session = Depends(get_db)):
    log = ComplianceService.get_audit_log_details(db, log_id)
    if not log:
        raise HTTPException(status_code=404, detail="Audit log not found")
    return log

# Compliance Checks
@app.post("/api/compliance/checks", response_model=CheckResponse, status_code=status.HTTP_201_CREATED)
def perform_compliance_check(check: CheckCreate, db: Session = Depends(get_db)):
    return ComplianceService.perform_compliance_check(db, check)

@app.get("/api/compliance/results/{check_id}", response_model=CheckResponse)
def get_check_result(check_id: int, db: Session = Depends(get_db)):
    check = ComplianceService.get_check_result(db, check_id)
    if not check:
        raise HTTPException(status_code=404, detail="Compliance check not found")
    return check

# Compliance Reports
@app.post("/api/reports/generate", response_model=ReportResponse, status_code=status.HTTP_201_CREATED)
def generate_compliance_report(report: ReportCreate):
    return ComplianceService.generate_compliance_report(report)

@app.get("/api/reports/{report_id}", response_model=ReportResponse)
def get_compliance_report(report_id: str):
    return ComplianceService.get_compliance_report(report_id)

# Risk Assessment
@app.post("/api/risk-assessment", response_model=RiskAssessmentResponse, status_code=status.HTTP_201_CREATED)
def start_risk_assessment(assessment: RiskAssessmentCreate, db: Session = Depends(get_db)):
    return ComplianceService.start_risk_assessment(db, assessment)

@app.get("/api/risk-assessment/results/{assessment_id}", response_model=RiskAssessmentResponse)
def get_risk_assessment(assessment_id: int, db: Session = Depends(get_db)):
    assessment = ComplianceService.get_risk_assessment(db, assessment_id)
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    return assessment

@app.get("/")
def root():
    return {"message": "Welcome to the Compliance and Audit Service"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)