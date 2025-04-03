from sqlalchemy.orm import Session
from models import ReferenceDocument
from datetime import datetime

def create_reference_document(
    db: Session,
    file_name: str,
    file_path: str,
    uploaded_by: int,
    toolbox_talk_id: int = None,
):
    doc = ReferenceDocument(
        file_name=file_name,
        file_path=file_path,
        uploaded_by=uploaded_by,
        toolbox_talk_id=toolbox_talk_id,
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc


def get_reference_documents(db: Session, skip: int = 0, limit: int = 10):
    return db.query(ReferenceDocument).offset(skip).limit(limit).all()

def delete_reference_document(db: Session, document_id: int):
    doc = db.query(ReferenceDocument).filter(ReferenceDocument.id == document_id).first()
    if doc:
        db.delete(doc)
        db.commit()
    return doc
