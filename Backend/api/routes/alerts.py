from fastapi import APIRouter, HTTPException, Depends
from typing import List
from ..models import Alert, AlertCreate, AlertResponse, User
from ..dependencies import get_current_user
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/alerts", response_model=List[AlertResponse])
async def get_alerts(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    alerts = db.query(Alert).all()
    return alerts

@router.post("/alerts", response_model=AlertResponse, status_code=201)
async def create_alert(alert: AlertCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_alert = Alert(**alert.dict())
    db.add(db_alert)
    db.commit()
    db.refresh(db_alert)
    return db_alert

