import logging
import traceback
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
        logger.info(f"Retrieved {len(products)} products")
        if not products:
            logger.warning("No products found in the database")
        product_list = [DeviceResponse(
            id=product.id,
            name=product.name,
            type=product.type,
            vendor_name=product.vendor.name if product.vendor else None
        ) for product in products]
        logger.info(f"Returning product list: {product_list}")
        return product_list
    except Exception as e:
        logger.error(f"Error retrieving products: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.post("/products", response_model=DeviceResponse)
def create_product(name: str, type: str, vendor_name: Optional[str] = None, db: Session = Depends(get_db)):
    try:
        logger.info(f"Attempting to create product: name={name}, type={type}, vendor_name={vendor_name}")
        vendor = None
        if vendor_name:
            vendor = db.query(Vendor).filter(Vendor.name == vendor_name).first()
            if not vendor:
                vendor = Vendor(name=vendor_name)
                db.add(vendor)
                db.commit()
                db.refresh(vendor)
                logger.info(f"Created new vendor: {vendor_name}")
            else:
                logger.info(f"Using existing vendor: {vendor_name}")

        product = Device(name=name, type=type, vendor=vendor)
        db.add(product)
        db.commit()
        db.refresh(product)
        logger.info(f"Successfully created product: id={product.id}, name={product.name}, type={product.type}, vendor={vendor.name if vendor else None}")
        return DeviceResponse(
            id=product.id,
            name=product.name,
            type=product.type,
            vendor_name=vendor.name if vendor else None
        )
    except Exception as e:
        logger.error(f"Error creating product: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

