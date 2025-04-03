# backend/routers/faiss_router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from crud import faiss as faiss_crud
from schemas.index_schema import IndexCreationRequest
from database import get_db
from crud.faiss import validate_toolbox_talk_exists  # Importamos la función auxiliar

router = APIRouter()

@router.post("/toolbox-talks/{toolbox_talk_id}/generate-index")
def create_faiss_index(
    toolbox_talk_id: int,
    index_request: IndexCreationRequest,
    db: Session = Depends(get_db)
):
    # Llamamos a la función auxiliar para validar que el Toolbox Talk exista
    validate_toolbox_talk_exists(toolbox_talk_id, db)

    # Llamamos al CRUD para crear el índice
    result = faiss_crud.create_faiss_index(db, toolbox_talk_id, index_request.document_ids)
    return result
