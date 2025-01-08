from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import json
from ..database import get_db
from ..models import ChangelogEntry, ChangelogEntryCreate, ChangelogEntryResponse, User, ChangelogChange
from ..dependencies import get_current_user

router = APIRouter()

@router.post("/changelog", response_model=ChangelogEntryResponse, status_code=status.HTTP_201_CREATED)
async def create_changelog_entry(
    entry: ChangelogEntryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can create changelog entries")
    
    new_entry = ChangelogEntry(version=entry.version, changes=json.dumps([change.dict() for change in entry.changes]))
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return new_entry

@router.get("/changelog", response_model=List[ChangelogEntryResponse])
async def get_changelog_entries(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    entries = db.query(ChangelogEntry).offset(skip).limit(limit).all()
    for entry in entries:
        entry.changes = json.loads(entry.changes)
        entry.changes = [ChangelogChange(**change) for change in entry.changes]
    return entries

@router.get("/changelog/{entry_id}", response_model=ChangelogEntryResponse)
async def get_changelog_entry(
    entry_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    entry = db.query(ChangelogEntry).filter(ChangelogEntry.id == entry_id).first()
    if entry is None:
        raise HTTPException(status_code=404, detail="Changelog entry not found")
    entry.changes = json.loads(entry.changes)
    entry.changes = [ChangelogChange(**change) for change in entry.changes]
    return entry

@router.put("/changelog/{entry_id}", response_model=ChangelogEntryResponse)
async def update_changelog_entry(
    entry_id: int,
    entry_update: ChangelogEntryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can update changelog entries")
    
    existing_entry = db.query(ChangelogEntry).filter(ChangelogEntry.id == entry_id).first()
    if existing_entry is None:
        raise HTTPException(status_code=404, detail="Changelog entry not found")
    
    existing_entry.version = entry_update.version
    existing_entry.changes = json.dumps([change.dict() for change in entry_update.changes])
    
    db.commit()
    db.refresh(existing_entry)
    existing_entry.changes = json.loads(existing_entry.changes)
    existing_entry.changes = [ChangelogChange(**change) for change in existing_entry.changes]
    return existing_entry

@router.delete("/changelog/{entry_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_changelog_entry(
    entry_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can delete changelog entries")
    
    entry = db.query(ChangelogEntry).filter(ChangelogEntry.id == entry_id).first()
    if entry is None:
        raise HTTPException(status_code=404, detail="Changelog entry not found")
    
    db.delete(entry)
    db.commit()
    return {"ok": True}

