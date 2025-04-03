from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SignatureBase(BaseModel):
    signer_name: str
    signer_email: Optional[str] = None
    signature_image: Optional[str] = None  # Base64 de la firma

class SignatureCreate(SignatureBase):
    toolbox_talk_id: int

class SignatureResponse(SignatureBase):
    id: int
    toolbox_talk_id: int
    signed_at: datetime  # ✅ Esto debe coincidir con models.py

    class Config:
        from_attributes = True

