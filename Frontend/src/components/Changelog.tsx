from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import ChangelogEntry, ChangelogEntryCreate, ChangelogEntryResponse, User
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
    
    new_entry = ChangelogEntry(**entry.dict())
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
    
    for key, value in entry_update.dict().items():
        setattr(existing_entry, key, value)
    
    db.commit()
    db.refresh(existing_entry)
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

