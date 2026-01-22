from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel, ConfigDict, field_validator
from typing import List, Optional, Dict, Any
from datetime import datetime
from .database import get_db, engine, Base
from .models import AuditLog
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
            return json.loads(v)
        return v

@app.post("/api/audit", response_model=AuditLogResponse)
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)