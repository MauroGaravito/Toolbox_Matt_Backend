from datetime import datetime
from typing import Optional
from pydantic import BaseModel

# 🔹 Esquema base para reutilizar
class DigitalSignatureBase(BaseModel):
    toolbox_talk_id: int
    full_name: str
    email: str

# 🔹 Esquema de entrada (POST) con imagen opcional
class DigitalSignatureCreate(DigitalSignatureBase):
    signature_image: Optional[str] = None  # 👈 este campo es CLAVE

# 🔹 Esquema de respuesta (GET)
class DigitalSignatureResponse(DigitalSignatureBase):
    id: int
    user_id: int
    signed_at: datetime

    class Config:
        orm_mode = True  # o from_attributes=True si estás en Pydantic v2
