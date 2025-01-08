from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc, or_
from typing import List, Optional
from ..database import get_db
from ..models import SearchQuery, PaginatedResponse, LogEntry, Device, Vendor, Customer, LogEntryResponse, User, SeverityEnum
from ..dependencies import get_current_user
from datetime import datetime, timedelta

router = APIRouter()

@router.get("/search", response_model=PaginatedResponse)
async def search_logs(
    query: str = Query(default=""),
    fields: Optional[List[str]] = Query(None),
    start_time: Optional[datetime] = Query(None),
    end_time: Optional[datetime] = Query(None),
    cnnid: Optional[str] = Query(None),
    vendor: Optional[str] = Query(None),
    device_type: Optional[str] = Query(None),
    severity: Optional[SeverityEnum] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    sort_by: str = Query("timestamp"),
    sort_order: str = Query("desc"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        # Start with a base query
        base_query = db.query(LogEntry).join(Device).join(Vendor).join(Customer)

        # Apply filters
        if query:
            if fields:
                conditions = []
                for field in fields:
                    if hasattr(LogEntry, field):
                        conditions.append(getattr(LogEntry, field).ilike(f"%{query}%"))
                base_query = base_query.filter(or_(*conditions))
            else:
                base_query = base_query.filter(LogEntry.message.ilike(f"%{query}%"))

        if start_time:
            base_query = base_query.filter(LogEntry.timestamp >= start_time)
        if end_time:
            base_query = base_query.filter(LogEntry.timestamp <= end_time)
        if cnnid:
            base_query = base_query.filter(Customer.cnnid == cnnid)
        if vendor:
            base_query = base_query.filter(Vendor.name == vendor)
        if device_type:
            base_query = base_query.filter(Device.type == device_type)
        if severity:
            base_query = base_query.filter(LogEntry.severity == severity)

        # Count total items
        total_items = base_query.count()

        # Apply sorting
        if not hasattr(LogEntry, sort_by):
            raise HTTPException(status_code=400, detail=f"Invalid sort_by field: {sort_by}")
        sort_column = getattr(LogEntry, sort_by)
        if sort_order.lower() == "asc":
            base_query = base_query.order_by(asc(sort_column))
        else:
            base_query = base_query.order_by(desc(sort_column))

        # Apply pagination
        logs = base_query.offset((page - 1) * page_size).limit(page_size).all()

        # Prepare response
        log_entries = [
            LogEntryResponse(
                id=log.id,
                timestamp=log.timestamp,
                message=log.message,
                severity=log.severity,
                device_name=log.device.name,
                device_type=log.device.type,
                vendor_name=log.device.vendor.name,
                customer_cnnid=log.device.vendor.customer.cnnid
            )
            for log in logs
        ]

        return PaginatedResponse(
            items=log_entries,
            total=total_items,
            page=page,
            page_size=page_size,
            total_pages=((total_items - 1) // page_size) + 1
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while searching logs: {str(e)}")

@router.get("/search/fields")
async def get_search_fields(current_user: User = Depends(get_current_user)):
    return {
        "log_fields": ["id", "timestamp", "message", "severity"],
        "device_fields": ["name", "type"],
        "vendor_fields": ["name"],
        "customer_fields": ["cnnid", "name"]
    }

@router.get("/search/recent")
async def get_recent_logs(
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        recent_logs = db.query(LogEntry).order_by(desc(LogEntry.timestamp)).limit(limit).all()
        return [
            LogEntryResponse(
                id=log.id,
                timestamp=log.timestamp,
                message=log.message,
                device_name=log.device.name,
                device_type=log.device.type,
                vendor_name=log.device.vendor.name,
                customer_cnnid=log.device.vendor.customer.cnnid
            )
            for log in recent_logs
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while fetching recent logs: {str(e)}")

@router.get("/search/timerange")
async def get_time_range_options():
    now = datetime.utcnow()
    return {
        "options": [
            {"label": "Last 15 minutes", "start_time": now - timedelta(minutes=15), "end_time": now},
            {"label": "Last hour", "start_time": now - timedelta(hours=1), "end_time": now},
            {"label": "Last 24 hours", "start_time": now - timedelta(days=1), "end_time": now},
            {"label": "Last 7 days", "start_time": now - timedelta(days=7), "end_time": now},
            {"label": "Last 30 days", "start_time": now - timedelta(days=30), "end_time": now},
        ]
    }

