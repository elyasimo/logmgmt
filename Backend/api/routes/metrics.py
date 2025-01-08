from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from ..models import Metric, MetricCreate, MetricResponse, LogEntry, User
from ..database import get_db
from ..dependencies import get_current_user

router = APIRouter()

@router.post("/metrics", response_model=MetricResponse)
async def create_metric(metric: MetricCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_metric = Metric(**metric.dict())
    db.add(db_metric)
    db.commit()
    db.refresh(db_metric)
    return db_metric

@router.get("/metrics", response_model=List[MetricResponse])
async def get_metrics(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    metrics = db.query(Metric).all()
    return metrics

@router.get("/metrics/log_levels", response_model=List[MetricResponse])
async def get_log_level_metrics(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    level_counts = db.query(LogEntry.level, func.count(LogEntry.level)).group_by(LogEntry.level).all()
    metrics = []
    for level, count in level_counts:
        metric = Metric(name=f"log_level_{level.lower()}", value=count)
        db.add(metric)
        metrics.append(metric)
    db.commit()
    return metrics

