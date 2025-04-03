from pydantic import BaseModel
from datetime import datetime

class ParticipantResponse(BaseModel):
    id: int
    user_id: int
    toolbox_talk_id: int
    assigned_at: datetime

    class Config:
        orm_mode = True
