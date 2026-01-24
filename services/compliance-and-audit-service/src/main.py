from fastapi import FastAPI, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, ConfigDict, field_validator
from typing import List, Optional, Dict, Any
from datetime import datetime
from .database import get_db, engine, Base
from .models import AuditLog, ComplianceCheck, RiskAssessment
import json

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

class AuditLogCreate(BaseModel):
    user_id: int
    action: str
    resource: Optional[str] = None
    details: Optional[Dict[str, Any]] = None

class AuditLogResponse(AuditLogCreate):
    id: int
    timestamp: datetime
    
    model_config = ConfigDict(from_attributes=True)

    @field_validator('details', mode='before')
    @classmethod
    def parse_details(cls, v):
        if isinstance(v, str):
            try:
                return json.loads(v)
            except:
                return v
        return v

class CheckCreate(BaseModel):
    check_type: str
    details: Optional[Dict[str, Any]] = None

class CheckResponse(CheckCreate):
    id: int
    status: str
    performed_at: datetime
    model_config = ConfigDict(from_attributes=True)

    @field_validator('details', mode='before')
    @classmethod
    def parse_details(cls, v):
        if isinstance(v, str):
            try:
                return json.loads(v)
            except:
                return v
        return v

class ReportCreate(BaseModel):
    report_type: str
    parameters: Optional[Dict[str, Any]] = None

class ReportResponse(BaseModel):
    id: str  # Mock returns string ID usually or URL
    download_url: str
    generated_at: datetime
    
class RiskAssessmentCreate(BaseModel):
    assessment_type: str
    details: Optional[Dict[str, Any]] = None

class RiskAssessmentResponse(RiskAssessmentCreate):
    id: int
    risk_score: int
    risk_level: str
    performed_at: datetime
    model_config = ConfigDict(from_attributes=True)

    @field_validator('details', mode='before')
    @classmethod
    def parse_details(cls, v):
        if isinstance(v, str):
            try:
                return json.loads(v)
            except:
                return v
        return v

@app.post("/api/audit", response_model=AuditLogResponse, status_code=status.HTTP_201_CREATED)
def create_audit_log(log: AuditLogCreate, db: Session = Depends(get_db)):
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

@app.get("/api/audit", response_model=List[AuditLogResponse])
def get_audit_logs(
    user_id: Optional[int] = Query(None),
    action: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(AuditLog)
    if user_id:
        query = query.filter(AuditLog.user_id == user_id)
    if action:
        query = query.filter(AuditLog.action == action)
    
    return query.all()

@app.get("/api/logs/{log_id}", response_model=AuditLogResponse)
def get_audit_log_details(log_id: int, db: Session = Depends(get_db)):
    log = db.query(AuditLog).filter(AuditLog.id == log_id).first()
    if not log:
        raise HTTPException(status_code=404, detail="Audit log not found")
    return log

# Compliance Checks
@app.post("/api/compliance/checks", response_model=CheckResponse, status_code=status.HTTP_201_CREATED)
def perform_compliance_check(check: CheckCreate, db: Session = Depends(get_db)):
    # Mock check logic
    # In reality, this would run rules. For now, random or fixed pass.
    db_check = ComplianceCheck(
        check_type=check.check_type,
        status="pass", 
        details=json.dumps(check.details) if check.details else None
    )
    db.add(db_check)
    db.commit()
    db.refresh(db_check)
    return db_check

@app.get("/api/compliance/results/{check_id}", response_model=CheckResponse)
def get_check_result(check_id: int, db: Session = Depends(get_db)):
    check = db.query(ComplianceCheck).filter(ComplianceCheck.id == check_id).first()
    if not check:
        raise HTTPException(status_code=404, detail="Compliance check not found")
    return check

# Compliance Reports
@app.post("/api/reports/generate", response_model=ReportResponse, status_code=status.HTTP_201_CREATED)
def generate_compliance_report(report: ReportCreate):
    # Mock report generation
    return ReportResponse(
        id=f"rep_{int(datetime.utcnow().timestamp())}",
        download_url=f"https://compliance.santhe.com/reports/{report.report_type}.pdf",
        generated_at=datetime.utcnow()
    )

@app.get("/api/reports/{report_id}", response_model=ReportResponse)
def get_compliance_report(report_id: str):
    # Mock retrieval
    return ReportResponse(
        id=report_id,
        download_url=f"https://compliance.santhe.com/reports/{report_id}.pdf",
        generated_at=datetime.utcnow()
    )

# Risk Assessment
@app.post("/api/risk-assessment", response_model=RiskAssessmentResponse, status_code=status.HTTP_201_CREATED)
def start_risk_assessment(assessment: RiskAssessmentCreate, db: Session = Depends(get_db)):
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

@app.get("/api/risk-assessment/results/{assessment_id}", response_model=RiskAssessmentResponse)
def get_risk_assessment(assessment_id: int, db: Session = Depends(get_db)):
    assessment = db.query(RiskAssessment).filter(RiskAssessment.id == assessment_id).first()
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    return assessment

@app.get("/")
def root():
    return {"message": "Welcome to the Compliance and Audit Service"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)