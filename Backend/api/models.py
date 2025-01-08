from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, JSON, Boolean, Enum
from sqlalchemy.orm import declarative_base, relationship
from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional, List
import re
import enum

Base = declarative_base()

class SeverityEnum(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    cnnid = Column(String, unique=True, index=True)
    name = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    vendors = relationship("Vendor", back_populates="customer")

class Vendor(Base):
    __tablename__ = "vendors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    customer = relationship("Customer", back_populates="vendors")
    devices = relationship("Device", back_populates="vendor")

class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    type = Column(String, index=True)
    vendor_id = Column(Integer, ForeignKey("vendors.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    vendor = relationship("Vendor", back_populates="devices")
    logs = relationship("LogEntry", back_populates="device")

class LogEntry(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, index=True, default=datetime.utcnow)
    message = Column(String)
    severity = Column(Enum(SeverityEnum), index=True)
    device_id = Column(Integer, ForeignKey("devices.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    device = relationship("Device", back_populates="logs")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String, default="user")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    query = Column(String)
    severity = Column(Enum(SeverityEnum))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Metric(Base):
    __tablename__ = "metrics"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    value = Column(Float)
    timestamp = Column(DateTime, index=True, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ChangelogEntry(Base):
    __tablename__ = "changelog_entries"

    id = Column(Integer, primary_key=True, index=True)
    version = Column(String, index=True)
    date = Column(DateTime, default=datetime.utcnow)
    changes = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Pydantic models

class LogEntryCreate(BaseModel):
    timestamp: datetime
    message: str
    severity: SeverityEnum
    device_id: int

class LogEntryResponse(BaseModel):
    id: int
    timestamp: datetime
    message: str
    severity: SeverityEnum
    device_name: str
    device_type: str
    vendor_name: str
    customer_cnnid: str

    class Config:
        orm_mode = True

class CustomerResponse(BaseModel):
    id: int
    cnnid: str
    name: Optional[str]

    class Config:
        orm_mode = True

class VendorResponse(BaseModel):
    id: int
    name: str
    customer_cnnid: str

    class Config:
        orm_mode = True

class DeviceResponse(BaseModel):
    id: int
    name: str
    type: str
    vendor_name: str

    class Config:
        orm_mode = True

class AlertCreate(BaseModel):
    name: str
    query: str
    severity: SeverityEnum

class AlertResponse(AlertCreate):
    id: int

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class UserInDB(UserBase):
    id: Optional[int] = None
    is_active: bool = True
    role: str = "user"

    class Config:
        orm_mode = True

class UserResponse(UserInDB):
    pass

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class MetricCreate(BaseModel):
    name: str
    value: float

class MetricResponse(MetricCreate):
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True

class SearchQuery(BaseModel):
    query: str = ""
    fields: Optional[List[str]] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    cnnid: Optional[str] = None
    vendor: Optional[str] = None
    device_type: Optional[str] = None
    severity: Optional[SeverityEnum] = None
    page: int = 1
    page_size: int = 10
    sort_by: str = "timestamp"
    sort_order: str = "desc"

class PaginatedResponse(BaseModel):
    items: List[LogEntryResponse]
    total: int
    page: int
    page_size: int
    total_pages: int

class ChangelogChange(BaseModel):
    type: str = Field(..., regex="^(added|changed|deprecated|removed|fixed|security)$")
    description: str = Field(..., min_length=1, max_length=500)

class ChangelogEntryCreate(BaseModel):
    version: str = Field(..., regex="^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$")
    changes: List[ChangelogChange]

    @validator('version')
    def version_must_be_semantic(cls, v):
        if not re.match(r'^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$', v):
            raise ValueError('Version must be a valid semantic version')
        return v

class ChangelogEntryResponse(BaseModel):
    id: int
    version: str
    date: datetime
    changes: List[ChangelogChange]

    class Config:
        orm_mode = True

