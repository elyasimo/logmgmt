from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

class LogSchema(BaseModel):
    LogEntry: dict

@router.get("/schemas", response_model=LogSchema)
async def get_schemas():
    return LogSchema(
        LogEntry={
            "timestamp": "string",
            "level": "string",
            "source": "string",
            "message": "string"
        }
    )

