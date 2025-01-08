from fastapi import APIRouter, HTTPException
from typing import List
from pydantic import BaseModel

router = APIRouter()

class LogSource(BaseModel):
    id: int
    name: str
    type: str
    configuration: dict

sources_db = []

@router.get("/sources", response_model=List[LogSource])
async def get_sources():
    return sources_db

@router.post("/sources", response_model=LogSource, status_code=201)
async def create_source(source: LogSource):
    source.id = len(sources_db) + 1
    sources_db.append(source)
    return source

