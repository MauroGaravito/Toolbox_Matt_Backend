from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas.reference_documents import ReferenceDocumentResponse
from crud.reference_documents import create_reference_document, get_reference_documents, delete_reference_document
from typing import List
from fastapi import UploadFile, File, Form
from datetime import datetime
import os

router = APIRouter(
    prefix="/reference_documents",
    tags=["Reference Documents"]
)

UPLOAD_DIR = "backend/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/", response_model=ReferenceDocumentResponse)
async def upload_reference_document(
    file: UploadFile = File(...),
    uploaded_by: int = Form(...),
    toolbox_talk_id: int = Form(None),
    db: Session = Depends(get_db),
):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"{timestamp}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    document = create_reference_document(
        db=db,
        file_name=filename,  # 👈 nombre final del archivo con timestamp
        file_path=file_path,
        uploaded_by=uploaded_by,
        toolbox_talk_id=toolbox_talk_id  # 👈 relación con Toolbox Talk
    )

    return document

@router.get("/", response_model=List[ReferenceDocumentResponse])
def read_reference_documents(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_reference_documents(db, skip=skip, limit=limit)

@router.delete("/{document_id}", response_model=ReferenceDocumentResponse)
def delete_existing_reference_document(document_id: int, db: Session = Depends(get_db)):
    db_document = delete_reference_document(db, document_id)
    if not db_document:
        raise HTTPException(status_code=404, detail="Document not found")
    return db_document
