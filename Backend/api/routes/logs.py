from fastapi import APIRouter, Request, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc, func, cast, Date, text, column
from Backend.api.database import get_db
from Backend.api.models import LogEntry, LogEntryCreate, LogEntryResponse, PaginatedResponse, Customer, Device, Vendor, SeverityEnum
from typing import List, Dict, Optional
import logging
import json
from datetime import datetime, timedelta, timezone
from sqlalchemy.exc import SQLAlchemyError, TimeoutError
import traceback
import csv
from io import StringIO
from fastapi.responses import Response

router = APIRouter()

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

@router.post("/logs", response_model=dict, summary="Create log entries")
async def create_log(request: Request, db: Session = Depends(get_db)):
    """
    Create new log entries.
    """
    try:
        body = await request.json()
        logs = body if isinstance(body, list) else [body]
        
        for log in logs:
            if 'vendor' not in log or 'product' not in log or 'cnnid' not in log:
                raise ValueError("Vendor, product, and cnnid fields are required for each log entry")
            
            # Ensure customer exists
            customer = db.query(Customer).filter(Customer.cnnid == log['cnnid']).first()
            if not customer:
                customer = Customer(cnnid=log['cnnid'], name=f"Customer {log['cnnid']}")
                db.add(customer)
                db.commit()
                db.refresh(customer)

            # Ensure product exists
            product = db.query(Device).filter(Device.name == log['product']).first()
            if not product:
                vendor = db.query(Vendor).filter(Vendor.name == log['vendor']).first()
                if not vendor:
                    vendor = Vendor(name=log['vendor'])
                    db.add(vendor)
                    db.commit()
                    db.refresh(vendor)
                product = Device(name=log['product'], type=log.get('device_type', 'unknown'), vendor=vendor)
                db.add(product)
                db.commit()
                db.refresh(product)

            log_entry = LogEntryCreate(
                timestamp=datetime.fromisoformat(log['timestamp']),
                message=log['message'],
                severity=SeverityEnum(log['severity']),
                device_id=product.id,
                vendor=log['vendor'],
                cnnid=log['cnnid'],
                product=log['product'],
                device_type=log.get('device_type', 'unknown')
            )
            db_log = LogEntry(**log_entry.dict())
            db.add(db_log)
            logger.debug(f"Inserted log: {db_log.vendor} - {db_log.timestamp} - {db_log.cnnid} - {db_log.product}")
        db.commit()
        logger.info(f"Received {len(logs)} log entries")
        return {"status": "success", "message": f"{len(logs)} log entries received and processed"}
    except Exception as e:
        logger.error(f"Error processing log entries: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Invalid log entries: {str(e)}")

@router.get("/logs", response_model=PaginatedResponse, summary="Get logs")
async def get_logs(
    query: Optional[str] = None,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    cnnid: Optional[str] = None,
    vendor: Optional[str] = None,
    device_type: Optional[str] = None,
    severity: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    sort_by: str = "timestamp",
    sort_order: str = "desc",
    db: Session = Depends(get_db)
):
    """
    Retrieve logs based on search criteria.
    """
    try:
        logger.debug(f"Received request with parameters: query={query}, vendor={vendor}, page={page}, page_size={page_size}, sort_by={sort_by}, sort_order={sort_order}")
    
        db_query = db.query(LogEntry)
    
        if query:
            db_query = db_query.filter(LogEntry.message.ilike(f"%{query}%"))
        if start_time:
            db_query = db_query.filter(LogEntry.timestamp >= start_time)
        if end_time:
            db_query = db_query.filter(LogEntry.timestamp <= end_time)
        if cnnid:
            db_query = db_query.filter(LogEntry.cnnid == cnnid)
        if vendor:
            db_query = db_query.filter(func.lower(LogEntry.vendor) == func.lower(vendor))
        if device_type:
            db_query = db_query.filter(LogEntry.device_type == device_type)
        if severity:
            db_query = db_query.filter(LogEntry.severity == severity)
    
        # Validate and apply sorting
        valid_columns = ['timestamp', 'severity', 'message', 'vendor', 'cnnid', 'device_type', 'product']
        if sort_by not in valid_columns:
            logger.warning(f"Invalid sort_by column: {sort_by}. Defaulting to 'timestamp'.")
            sort_by = 'timestamp'
    
        sort_column = getattr(LogEntry, sort_by)
        if sort_order.lower() == "asc":
            db_query = db_query.order_by(sort_column)
        else:
            db_query = db_query.order_by(desc(sort_column))
    
        total = db_query.count()
        logger.debug(f"Total logs found: {total}")
    
        logs = db_query.offset((page - 1) * page_size).limit(page_size).all()
        logger.debug(f"Logs retrieved: {len(logs)}")
    
        log_entries = [LogEntryResponse.from_orm(log) for log in logs]
        logger.debug(f"Log entries created: {len(log_entries)}")
    
        response = PaginatedResponse(
            items=log_entries,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=(total + page_size - 1) // page_size
        )
        logger.debug(f"Response created: {response}")
    
        return response
    except SQLAlchemyError as e:
        logger.error(f"Database error in get_logs: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Database error occurred: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error in get_logs: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

@router.get("/logs/count", response_model=dict, summary="Get total log count")
async def get_log_count(db: Session = Depends(get_db)):
    """
    Get the total count of log entries.
    """
    count = db.query(LogEntry).count()
    logger.debug(f"Total log count: {count}")
    return {"total_logs": count}

@router.get("/logs/vendors", response_model=List[str], summary="Get unique vendors")
async def get_vendors(db: Session = Depends(get_db)):
    """
    Get a list of unique vendors.
    """
    vendors = db.query(LogEntry.vendor).distinct().filter(LogEntry.vendor != None).all()
    vendor_list = [vendor[0] for vendor in vendors]
    logger.debug(f"Unique vendors: {vendor_list}")
    return vendor_list

@router.get("/logs/vendor-counts", response_model=Dict[str, int], summary="Get log counts by vendor")
def get_log_counts_by_vendor(
    start_date: datetime = Query(default=None, description="Start date for the count (inclusive)"),
    end_date: datetime = Query(default=None, description="End date for the count (inclusive)"),
    db: Session = Depends(get_db)
):
    logger.debug(f"get_log_counts_by_vendor called with start_date={start_date}, end_date={end_date}")
    if start_date:
        start_date = start_date.replace(tzinfo=timezone.utc)
    if end_date:
        end_date = end_date.replace(tzinfo=timezone.utc)
    logger.debug(f"Adjusted start_date: {start_date}, end_date: {end_date}")

    try:
        query = db.query(LogEntry.vendor, func.count(LogEntry.id).label('count'))
        
        if start_date:
            query = query.filter(LogEntry.timestamp >= start_date)
        if end_date:
            query = query.filter(LogEntry.timestamp <= end_date)
        
        query = query.filter(LogEntry.vendor != None).group_by(LogEntry.vendor)
        
        logger.debug(f"Executing query: {query}")
        result = query.all()
        logger.debug(f"Query execution completed. Raw result: {result}")
        
        vendor_counts = {vendor: count for vendor, count in result if vendor is not None}
        logger.debug(f"Processed vendor counts: {vendor_counts}")
        return vendor_counts

    except SQLAlchemyError as e:
        logger.error(f"SQLAlchemy error executing query: {e}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Database error occurred: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error in get_log_counts_by_vendor: {e}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

@router.get("/logs/severity-distribution", response_model=Dict[str, int], summary="Get severity distribution")
async def get_severity_distribution(
    start_date: datetime = Query(default=None, description="Start date for the distribution (inclusive)"),
    end_date: datetime = Query(default=None, description="End date for the distribution (inclusive)"),
    db: Session = Depends(get_db)
):
    logger.debug(f"get_severity_distribution called with start_date={start_date}, end_date={end_date}")
    if start_date:
        start_date = start_date.replace(tzinfo=timezone.utc)
    if end_date:
        end_date = end_date.replace(tzinfo=timezone.utc)
    logger.debug(f"Adjusted start_date: {start_date}, end_date: {end_date}")

    query = text("""
        SELECT severity, COUNT(*) as count
        FROM logs
        WHERE (:start_date IS NULL OR timestamp >= :start_date)
          AND (:end_date IS NULL OR timestamp <= :end_date)
        GROUP BY severity
    """)

    logger.debug(f"SQL Query: {query}")

    result = db.execute(query, {"start_date": start_date, "end_date": end_date}).fetchall()
    
    logger.debug(f"Raw severity distribution result: {result}")
    severity_distribution = {severity: count for severity, count in result if severity is not None}
    logger.debug(f"Processed severity distribution: {severity_distribution}")
    return severity_distribution

@router.get("/logs/time-series", response_model=Dict[str, int], summary="Get log count time series")
async def get_log_count_time_series(
    start_date: datetime = Query(default=None, description="Start date for the time series (inclusive)"),
    end_date: datetime = Query(default=None, description="End date for the time series (inclusive)"),
    interval: str = Query("day", description="Interval for the time series (day, hour, or minute)"),
    db: Session = Depends(get_db)
):
    logger.debug(f"get_log_count_time_series called with start_date={start_date}, end_date={end_date}, interval={interval}")
    if interval not in ["day", "hour", "minute"]:
        raise HTTPException(status_code=400, detail="Invalid interval. Must be 'day', 'hour', or 'minute'.")

    if not start_date:
        start_date = datetime.now(timezone.utc) - timedelta(days=7)
    if not end_date:
        end_date = datetime.now(timezone.utc)

    start_date = start_date.replace(tzinfo=timezone.utc)
    end_date = end_date.replace(tzinfo=timezone.utc)
    logger.debug(f"Adjusted start_date: {start_date}, end_date: {end_date}")

    query = text(f"""
        SELECT strftime(:date_format, timestamp, 'unixepoch') as interval_timestamp, COUNT(*) as count
        FROM logs
        WHERE timestamp >= :start_date AND timestamp <= :end_date
        GROUP BY interval_timestamp
        ORDER BY interval_timestamp
    """)

    if interval == "day":
        date_format = '%Y-%m-%d'
    elif interval == "hour":
        date_format = '%Y-%m-%d %H:00:00'
    else:  # minute
        date_format = '%Y-%m-%d %H:%M:00'

    logger.debug(f"SQL Query: {query}")
    logger.debug(f"Query parameters: date_format={date_format}, start_date={start_date}, end_date={end_date}")

    result = db.execute(query, {
        "date_format": date_format,
        "start_date": start_date.timestamp(),
        "end_date": end_date.timestamp()
    }).fetchall()
    
    logger.debug(f"Raw time series result: {result}")
    time_series = {str(timestamp): count for timestamp, count in result}
    logger.debug(f"Processed time series: {time_series}")
    return time_series

@router.get("/logs/export", response_model=None, summary="Export logs as CSV")
async def export_logs(
    query: Optional[str] = None,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    cnnid: Optional[str] = None,
    vendor: Optional[str] = None,
    device_type: Optional[str] = None,
    severity: Optional[str] = None,
    sort_by: str = "timestamp",
    sort_order: str = "desc",
    db: Session = Depends(get_db)
):
    """
    Export logs as CSV based on the provided filters.
    """
    try:
        # Create query with filters
        db_query = db.query(LogEntry)
        
        if query:
            db_query = db_query.filter(LogEntry.message.ilike(f"%{query}%"))
        if start_time:
            db_query = db_query.filter(LogEntry.timestamp >= start_time)
        if end_time:
            db_query = db_query.filter(LogEntry.timestamp <= end_time)
        if cnnid:
            db_query = db_query.filter(LogEntry.cnnid == cnnid)
        if vendor:
            db_query = db_query.filter(func.lower(LogEntry.vendor) == func.lower(vendor))
        if device_type:
            db_query = db_query.filter(LogEntry.device_type == device_type)
        if severity:
            db_query = db_query.filter(LogEntry.severity == severity)
        
        # Validate sort_by column exists
        valid_columns = ['timestamp', 'severity', 'message', 'vendor', 'cnnid', 'device_type']
        if sort_by not in valid_columns:
            sort_by = 'timestamp'  # Default to timestamp if invalid column
        
        # Apply sorting
        if sort_order.lower() == "asc":
            db_query = db_query.order_by(getattr(LogEntry, sort_by))
        else:
            db_query = db_query.order_by(desc(getattr(LogEntry, sort_by)))
        
        # Get all matching logs
        logs = db_query.all()
        
        # Create CSV content
        output = StringIO()
        writer = csv.writer(output)
        
        # Write headers
        writer.writerow(['Timestamp', 'Severity', 'Message', 'Vendor', 'CNNID', 'Device Type'])
        
        # Write data
        for log in logs:
            writer.writerow([
                log.timestamp.isoformat(),
                log.severity,
                log.message,
                log.vendor,
                log.cnnid,
                log.device_type
            ])
        
        # Get the CSV content
        csv_content = output.getvalue()
        output.close()
        
        # Prepare response
        return Response(
            content=csv_content,
            media_type='text/csv',
            headers={
                'Content-Disposition': f'attachment; filename=logs-export-{datetime.now().strftime("%Y%m%d-%H%M%S")}.csv'
            }
        )
        
    except Exception as e:
        logger.error(f"Error exporting logs: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Failed to export logs: {str(e)}")

