from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..models import LogEntry, LogEntryCreate, Customer, Vendor, Device
from ..dependencies import get_current_user
from ..database import get_db
from typing import List
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

def get_or_create_customer(db: Session, cnnid: str):
    customer = db.query(Customer).filter(Customer.cnnid == cnnid).first()
    if not customer:
        customer = Customer(cnnid=cnnid)
        db.add(customer)
        db.commit()
        db.refresh(customer)
    return customer

def get_or_create_vendor(db: Session, name: str, customer: Customer):
    vendor = db.query(Vendor).filter(Vendor.name == name, Vendor.customer_id == customer.id).first()
    if not vendor:
        vendor = Vendor(name=name, customer_id=customer.id)
        db.add(vendor)
        db.commit()
        db.refresh(vendor)
    return vendor

def get_or_create_device(db: Session, name: str, device_type: str, vendor: Vendor):
    device = db.query(Device).filter(Device.name == name, Device.vendor_id == vendor.id).first()
    if not device:
        device = Device(name=name, type=device_type, vendor_id=vendor.id)
        db.add(device)
        db.commit()
        db.refresh(device)
    return device

@router.post("/ingest", status_code=201)
async def ingest_logs(logs: List[LogEntryCreate], db: Session = Depends(get_db)):
    try:
        for log in logs:
            customer = get_or_create_customer(db, log.cnnid)
            vendor = get_or_create_vendor(db, log.vendor, customer)
            device = get_or_create_device(db, log.device_name, log.device_type, vendor)

            db_log = LogEntry(
                timestamp=log.timestamp,
                message=log.message,
                device_id=device.id
            )
            db.add(db_log)

        db.commit()
        logger.info(f"Ingested {len(logs)} log entries")
        return {"message": f"Successfully ingested {len(logs)} log entries"}
    except Exception as e:
        logger.error(f"Error ingesting logs: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to ingest logs: {str(e)}")

