from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..models import LogEntry, User
from ..database import get_db
from ..dependencies import get_current_user
from datetime import datetime, timedelta

router = APIRouter()

@router.get("/dashboard/stats")
async def get_dashboard_stats(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    total_logs = db.query(func.count(LogEntry.id)).scalar()
    unique_users = db.query(func.count(func.distinct(User.id))).scalar()
    
    # Calculate average logs per day for the last 30 days
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    logs_last_30_days = db.query(func.count(LogEntry.id)).filter(LogEntry.timestamp >= thirty_days_ago).scalar()
    avg_logs_per_day = logs_last_30_days / 30 if logs_last_30_days else 0

    return {
        "totalLogs": total_logs,
        "uniqueUsers": unique_users,
        "averageLogsPerDay": round(avg_logs_per_day, 2)
    }

