from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from schemas.activity_logs import ActivityLogCreate, ActivityLogResponse
from crud.activity_logs import create_activity_log, get_activity_logs
from typing import List

router = APIRouter(
    prefix="/activity_logs",
    tags=["Activity Logs"]
)

@router.post("/", response_model=ActivityLogResponse)
def log_activity(activity_log: ActivityLogCreate, db: Session = Depends(get_db)):
    return create_activity_log(db, activity_log)

@router.get("/", response_model=List[ActivityLogResponse])
def read_activity_logs(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_activity_logs(db, skip=skip, limit=limit)
