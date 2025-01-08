from fastapi import APIRouter, HTTPException
from typing import List
from pydantic import BaseModel

router = APIRouter()

class Dashboard(BaseModel):
    id: int
    name: str
    widgets: List[dict]

dashboards_db = []

@router.get("/dashboards", response_model=List[Dashboard])
async def get_dashboards():
    return dashboards_db

@router.post("/dashboards", response_model=Dashboard, status_code=201)
async def create_dashboard(dashboard: Dashboard):
    dashboard.id = len(dashboards_db) + 1
    dashboards_db.append(dashboard)
    return dashboard

