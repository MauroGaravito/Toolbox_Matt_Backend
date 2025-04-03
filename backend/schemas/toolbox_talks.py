from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from .reference_documents import ReferenceDocumentResponse
from .digital_signatures import DigitalSignatureResponse  # ✅ Importación
from .signatures import SignatureResponse  # ✅ Importación


class ToolboxTalkBase(BaseModel):
    topic: str
    content: str


class ToolboxTalkCreate(ToolboxTalkBase):
    created_by: int


class ToolboxTalkUpdate(BaseModel):
    topic: Optional[str] = None
    content: Optional[str] = None


class ToolboxTalkResponse(ToolboxTalkBase):
    id: int
    created_by: int
    created_at: datetime
    documents: List[ReferenceDocumentResponse] = []
    signatures: List[SignatureResponse] = []  # 🖊️ con imagen
    digital_signatures: List[DigitalSignatureResponse] = []  # ✍️ sin imagen

    class Config:
        from_attributes = True
