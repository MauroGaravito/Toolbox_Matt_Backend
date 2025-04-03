from pydantic import BaseModel
from datetime import datetime

class ActivityLogBase(BaseModel):
    user_id: int
    action: str

class ActivityLogCreate(ActivityLogBase):
    pass

class ActivityLogResponse(ActivityLogBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True
