from pydantic import BaseModel

class IndexCreationRequest(BaseModel):
    toolbox_talk_id: int  # Relación con el Toolbox Talk
    document_ids: list[int]  # IDs de los documentos que serán procesados
