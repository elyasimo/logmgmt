from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..models import LogEntry, User, Device, Vendor, Customer
from ..database import get_db
from ..dependencies import get_current_user
from typing import List
from datetime import datetime, timedelta

router = APIRouter()

@router.get("/statistics")
async def get_log_statistics(
    start_time: datetime = None,
    end_time: datetime = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(LogEntry).join(Device).join(Vendor).join(Customer)

    if start_time:
        query = query.filter(LogEntry.timestamp >= start_time)
    if end_time:
        query = query.filter(LogEntry.timestamp <= end_time)

    total_logs = query.count()
    
    device_counts = (
        query.with_entities(Device.type, func.count(LogEntry.id))
        .group_by(Device.type)
        .all()
    )
    
    vendor_counts = (
        query.with_entities(Vendor.name, func.count(LogEntry.id))
        .group_by(Vendor.name)
        .all()
    )
    
    customer_counts = (
        query.with_entities(Customer.cnnid, func.count(LogEntry.id))
        .group_by(Customer.cnnid)
        .all()
    )

    # Get log counts for the last 7 days
    today = datetime.utcnow().date()
    last_week = today - timedelta(days=7)
    daily_counts = (
        query.with_entities(func.date(LogEntry.timestamp), func.count(LogEntry.id))
        .filter(func.date(LogEntry.timestamp) >= last_week)
        .group_by(func.date(LogEntry.timestamp))
        .all()
    )

    return {
        "total_logs": total_logs,
        "device_type_distribution": dict(device_counts),
        "vendor_distribution": dict(vendor_counts),
        "customer_distribution": dict(customer_counts),
        "daily_log_counts": dict(daily_counts)
    }

