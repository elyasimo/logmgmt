from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, JSON, Boolean, Enum, Table
from sqlalchemy.orm import declarative_base, relationship
from pydantic import BaseModel, Field, validator, EmailStr
from datetime import datetime
from typing import Optional, List
import re
import enum

Base = declarative_base()

# Association table for many-to-many relationship between User and Group
user_group = Table('user_group', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('group_id', Integer, ForeignKey('groups.id'))
)

class SeverityEnum(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"

class AuthMethod(str, enum.Enum):
    local = "local"
    ldap = "ldap"
    active_directory = "active_directory"
    sso = "sso"
    azure_ad = "azure_ad"

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    cnnid = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    vendors = relationship("Vendor", back_populates="customer")

class Vendor(Base):
    __tablename__ = "vendors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    customer = relationship("Customer", back_populates="vendors")
    devices = relationship("Device", back_populates="vendor")

class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    type = Column(String, index=True, nullable=False)
    vendor_id = Column(Integer, ForeignKey("vendors.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    vendor = relationship("Vendor", back_populates="devices")
    logs = relationship("LogEntry", back_populates="device")

class LogEntry(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, index=True, nullable=False)
    message = Column(String, nullable=False)
    severity = Column(Enum(SeverityEnum), index=True, nullable=False)
    device_id = Column(Integer, ForeignKey("devices.id"), nullable=False)
    cnnid = Column(String, index=True, nullable=True)
    location = Column(String, index=True)
    city = Column(String, index=True)
    product = Column(String, index=True, nullable=True)
    device_number = Column(String)
    vendor = Column(String, index=True, nullable=True)
    device_type = Column(String, index=True, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    device = relationship("Device", back_populates="logs")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    name = Column(String, index=True)
    is_active = Column(Boolean, default=True)
    role = Column(String, default="user")
    auth_method = Column(Enum(AuthMethod), default=AuthMethod.local)
    external_id = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    groups = relationship("Group", secondary=user_group, back_populates="users")

class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    users = relationship("User", secondary=user_group, back_populates="groups")

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    query = Column(String, nullable=False)
    severity = Column(Enum(SeverityEnum), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Metric(Base):
    __tablename__ = "metrics"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    value = Column(Float, nullable=False)
    timestamp = Column(DateTime, index=True, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ChangelogEntry(Base):
    __tablename__ = "changelog_entries"

    id = Column(Integer, primary_key=True, index=True)
    version = Column(String, index=True, nullable=False)
    date = Column(DateTime, default=datetime.utcnow)
    changes = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Pydantic models

class LogEntryCreate(BaseModel):
    timestamp: datetime
    message: str
    severity: SeverityEnum
    device_id: int
    vendor: Optional[str] = None
    cnnid: Optional[str] = None
    location: Optional[str] = None
    city: Optional[str] = None
    product: Optional[str] = None
    device_number: Optional[str] = None
    device_type: Optional[str] = None

class LogEntryResponse(BaseModel):
    id: int
    timestamp: datetime
    message: str
    severity: SeverityEnum
    vendor: Optional[str] = None
    cnnid: Optional[str] = None
    product: Optional[str] = None
    device_type: Optional[str] = None
    location: Optional[str] = None
    city: Optional[str] = None
    device_number: Optional[str] = None

    class Config:
        orm_mode = True

class PaginatedResponse(BaseModel):
    items: List[LogEntryResponse]
    total: int
    page: int
    page_size: int
    total_pages: int

class SearchQuery(BaseModel):
    query: str = ""
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

class CustomerResponse(BaseModel):
    id: int
    cnnid: str
    name: str

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
    email: EmailStr
    name: str

class UserCreate(UserBase):
    password: str
    role: str = "user"
    auth_method: AuthMethod = AuthMethod.local
    external_id: Optional[str] = None

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None
    id: Optional[int] = None
    class Config:
        extra = "ignore"

class UserInDB(UserBase):
    id: int
    is_active: bool = True
    role: str = "user"
    auth_method: AuthMethod
    external_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class UserResponse(UserInDB):
    pass

class GroupBase(BaseModel):
    name: str
    description: str

class GroupCreate(GroupBase):
    pass

class GroupUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class GroupInDB(GroupBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class GroupResponse(GroupInDB):
    users: List[UserResponse] = []

class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str

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

