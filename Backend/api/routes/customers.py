from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Backend.api.database import get_db
from Backend.api.models import Customer, CustomerResponse

router = APIRouter()

@router.get("/customers", response_model=list[CustomerResponse])
def get_customers(db: Session = Depends(get_db)):
    customers = db.query(Customer).all()
    return customers

@router.get("/customers/{cnnid}", response_model=CustomerResponse)
def get_customer(cnnid: str, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.cnnid == cnnid).first()
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@router.post("/customers", response_model=CustomerResponse)
def create_customer(cnnid: str, name: str, db: Session = Depends(get_db)):
    customer = Customer(cnnid=cnnid, name=name)
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer

