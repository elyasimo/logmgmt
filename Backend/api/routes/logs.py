from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from ..models import LogEntry, LogEntryCreate, LogEntryResponse, User
from ..dependencies import get_current_user
from ..database import get_db
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/logs", response_model=LogEntryResponse)
async def ingest_log(log_entry: LogEntryCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        db_log = LogEntry(**log_entry.dict())
        db.add(db_log)
        db.commit()
        db.refresh(db_log)
        logger.info(f"Log ingested: {db_log.id}")
        return LogEntryResponse.from_orm(db_log)
    except Exception as e:
        logger.error(f"Error ingesting log: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to ingest log: {str(e)}")

@router.get("/logs", response_model=List[LogEntryResponse])
async def get_logs(skip: int = 0, limit: int = 100, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    logs = db.query(LogEntry).offset(skip).limit(limit).all()
    return [LogEntryResponse.from_orm(log) for log in logs]

