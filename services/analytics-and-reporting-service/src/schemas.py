from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict, Any
from datetime import datetime

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
