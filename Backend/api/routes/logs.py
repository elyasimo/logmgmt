from fastapi import APIRouter, Request, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from Backend.api.database import get_db
from Backend.api.models import LogEntry, LogEntryCreate, LogEntryResponse, SearchQuery, PaginatedResponse
from typing import List
import logging
import json
from datetime import datetime

router = APIRouter()

# Configure logging
logger = logging.getLogger(__name__)

@router.post("/logs", response_model=dict)
async def create_log(request: Request, db: Session = Depends(get_db)):
    try:
        body = await request.body()
        logs = [json.loads(line) for line in body.decode().split('\n') if line]
        for log in logs:
            log_entry = LogEntryCreate(
                timestamp=datetime.fromisoformat(log['timestamp']),
                message=log['message'],
                severity=log.get('severity', 'low'),
                device_id=1,  # You may want to update this based on your needs
                vendor=log['vendor'],
                cnnid=log.get('cnnid', ''),
                location=log.get('location', ''),
                city=log.get('city', ''),
                product=log.get('product', ''),
                device_number=log.get('device_number', ''),
                device_type=log.get('device_type', '')
            )
            db_log = LogEntry(**log_entry.dict())
            db.add(db_log)
            logger.debug(f"Inserted log: {db_log.vendor} - {db_log.timestamp}")
        db.commit()
        logger.info(f"Received {len(logs)} log entries")
        return {"status": "success", "message": f"{len(logs)} log entries received and processed"}
    except Exception as e:
        logger.error(f"Error processing log entries: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Invalid log entries: {str(e)}")

@router.get("/logs", response_model=PaginatedResponse)
async def get_logs(
    search: SearchQuery = Depends(),
    db: Session = Depends(get_db)
):
    query = db.query(LogEntry)
    
    logger.debug(f"Query parameters: vendor={search.vendor}, page={search.page}, page_size={search.page_size}")
    
    if search.query:
        query = query.filter(LogEntry.message.ilike(f"%{search.query}%"))
    if search.start_time:
        query = query.filter(LogEntry.timestamp >= search.start_time)
    if search.end_time:
        query = query.filter(LogEntry.timestamp <= search.end_time)
    if search.cnnid:
        query = query.filter(LogEntry.cnnid == search.cnnid)
    if search.vendor:
        query = query.filter(func.lower(LogEntry.vendor) == func.lower(search.vendor))
    if search.device_type:
        query = query.filter(LogEntry.device_type == search.device_type)
    if search.severity:
        query = query.filter(LogEntry.severity == search.severity)
    
    total = query.count()
    logger.debug(f"Total logs found: {total}")
    
    if search.sort_order.lower() == "asc":
        query = query.order_by(getattr(LogEntry, search.sort_by))
    else:
        query = query.order_by(desc(getattr(LogEntry, search.sort_by)))
    
    logs = query.offset((search.page - 1) * search.page_size).limit(search.page_size).all()
    logger.debug(f"Logs retrieved: {len(logs)}")
    
    return PaginatedResponse(
        items=[LogEntryResponse.from_orm(log) for log in logs],
        total=total,
        page=search.page,
        page_size=search.page_size,
        total_pages=(total + search.page_size - 1) // search.page_size
    )

@router.get("/logs/count", response_model=dict)
async def get_log_count(db: Session = Depends(get_db)):
    count = db.query(LogEntry).count()
    logger.debug(f"Total log count: {count}")
    return {"total_logs": count}

@router.get("/logs/vendors", response_model=List[str])
async def get_vendors(db: Session = Depends(get_db)):
    vendors = db.query(LogEntry.vendor).distinct().filter(LogEntry.vendor != None).all()
    vendor_list = [vendor[0] for vendor in vendors]
    logger.debug(f"Unique vendors: {vendor_list}")
    return vendor_list

