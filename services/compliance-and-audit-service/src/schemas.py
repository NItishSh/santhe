from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional, Dict, Any
from datetime import datetime
import json

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
    id: str  
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
