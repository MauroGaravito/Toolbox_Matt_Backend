from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from security import get_current_user
from schemas.digital_signatures import DigitalSignatureCreate, DigitalSignatureResponse
from crud.digital_signatures import create_signature, get_signatures_by_toolbox_talk
from models import User

router = APIRouter(prefix="/digital-signatures", tags=["Digital Signatures"])

@router.post("/", response_model=DigitalSignatureResponse, status_code=status.HTTP_201_CREATED)
def sign_toolbox_talk(
    signature_data: DigitalSignatureCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_signature(db, user=current_user, signature_data=signature_data)

@router.get("/toolbox-talk/{toolbox_talk_id}", response_model=list[DigitalSignatureResponse])
def list_signatures(toolbox_talk_id: int, db: Session = Depends(get_db)):
    signatures = get_signatures_by_toolbox_talk(db, toolbox_talk_id)
    return signatures

@router.delete("/{signature_id}", status_code=204)
def delete_signature(
    signature_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    from models import Signature

    signature = db.query(Signature).filter(Signature.id == signature_id).first()
    if not signature:
        raise HTTPException(status_code=404, detail="Signature not found")

    db.delete(signature)
    db.commit()
    return {"message": "Signature deleted successfully"}

