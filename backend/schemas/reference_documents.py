from pydantic import BaseModel
from datetime import datetime

class ReferenceDocumentResponse(BaseModel):
    id: int
    file_name: str
    file_path: str
    uploaded_by: int
    uploaded_at: datetime

    class Config:
        from_attributes = True
