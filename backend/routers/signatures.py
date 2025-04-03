from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from schemas.signatures import SignatureCreate, SignatureResponse
from crud.signatures import (
    create_signature,
    get_signatures,
    get_signatures_by_toolbox_talk,
    delete_signature,
)

router = APIRouter(
    prefix="/signatures",
    tags=["Signatures"]
)

# 🔸 Cargar una firma con imagen
@router.post("/", response_model=SignatureResponse)
def upload_signature(signature: SignatureCreate, db: Session = Depends(get_db)):
    return create_signature(db, signature)

# 🔸 Obtener todas las firmas (admin o pruebas)
@router.get("/", response_model=List[SignatureResponse])
def read_signatures(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_signatures(db, skip=skip, limit=limit)

# 🔸 Obtener firmas por Toolbox Talk específico (frontend)
@router.get("/toolbox-talk/{toolbox_talk_id}", response_model=List[SignatureResponse])
def list_signatures_for_talk(toolbox_talk_id: int, db: Session = Depends(get_db)):
    return get_signatures_by_toolbox_talk(db, toolbox_talk_id)

# 🔸 Eliminar una firma por ID
@router.delete("/{signature_id}", response_model=SignatureResponse)
def delete_existing_signature(signature_id: int, db: Session = Depends(get_db)):
    db_signature = delete_signature(db, signature_id)
    if not db_signature:
        raise HTTPException(status_code=404, detail="Signature not found")
    return db_signature

# 🔸 Eliminar firma (con y sin imagen) por toolbox_talk_id + email
@router.delete("/by-toolbox-talk/{toolbox_talk_id}/email/{email}")
def delete_signature_by_toolbox_and_email(toolbox_talk_id: int, email: str, db: Session = Depends(get_db)):
    from models import Signature, DigitalSignature

    sig = db.query(Signature).filter(
        Signature.toolbox_talk_id == toolbox_talk_id,
        Signature.signer_email == email
    ).first()

    dig = db.query(DigitalSignature).filter(
        DigitalSignature.toolbox_talk_id == toolbox_talk_id,
        DigitalSignature.email == email
    ).first()

    if not sig and not dig:
        raise HTTPException(status_code=404, detail="No signature found.")

    if sig:
        db.delete(sig)
    if dig:
        db.delete(dig)

    db.commit()
    return {"message": "Signature(s) deleted"}
