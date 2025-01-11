import logging
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from Backend.api.database import get_db
from Backend.api.models import Device, Vendor

logger = logging.getLogger(__name__)

class DeviceResponse(BaseModel):
    id: int
    name: str
    type: str
    vendor_name: Optional[str]

    class Config:
        orm_mode = True

router = APIRouter()

@router.get("/products", response_model=List[DeviceResponse])
def get_products(db: Session = Depends(get_db)):
    try:
        products = db.query(Device).all()
        return [DeviceResponse(
            id=product.id,
            name=product.name,
            type=product.type,
            vendor_name=product.vendor.name if product.vendor else None
        ) for product in products]
    except Exception as e:
        logger.error(f"Error retrieving products: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/products", response_model=DeviceResponse)
def create_product(name: str, type: str, vendor_name: Optional[str] = None, db: Session = Depends(get_db)):
    try:
        vendor = None
        if vendor_name:
            vendor = db.query(Vendor).filter(Vendor.name == vendor_name).first()
            if not vendor:
                vendor = Vendor(name=vendor_name)
                db.add(vendor)
                db.commit()
                db.refresh(vendor)

        product = Device(name=name, type=type, vendor=vendor)
        db.add(product)
        db.commit()
        db.refresh(product)
        return DeviceResponse(
            id=product.id,
            name=product.name,
            type=product.type,
            vendor_name=vendor.name if vendor else None
        )
    except Exception as e:
        logger.error(f"Error creating product: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

