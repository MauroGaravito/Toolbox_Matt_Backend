from sqlalchemy.orm import Session
from models import Signature, DigitalSignature
from schemas.signatures import SignatureCreate

def create_signature(db: Session, signature: SignatureCreate):
    """Guarda una firma con imagen en la base de datos."""
    db_signature = Signature(
        toolbox_talk_id=signature.toolbox_talk_id,
        signer_name=signature.signer_name,
        signer_email=signature.signer_email,
        signature_image=signature.signature_image
    )
    db.add(db_signature)
    db.commit()
    db.refresh(db_signature)
    return db_signature

def get_signatures(db: Session, skip: int = 0, limit: int = 10):
    """Obtiene todas las firmas (útil para administración)."""
    return db.query(Signature).offset(skip).limit(limit).all()

def get_signatures_by_toolbox_talk(db: Session, toolbox_talk_id: int):
    """Obtiene las firmas asociadas a un Toolbox Talk específico."""
    return db.query(Signature).filter(Signature.toolbox_talk_id == toolbox_talk_id).all()

def delete_signature(db: Session, signature_id: int):
    """Elimina una firma por ID, incluyendo su vínculo en digital_signatures si existe."""
    db_signature = db.query(Signature).filter(Signature.id == signature_id).first()
    if db_signature:
        # También eliminar de digital_signatures si coincide toolbox_talk_id y email
        digital_sig = db.query(DigitalSignature).filter(
            DigitalSignature.toolbox_talk_id == db_signature.toolbox_talk_id,
            DigitalSignature.email == db_signature.signer_email
        ).first()
        if digital_sig:
            db.delete(digital_sig)

        db.delete(db_signature)
        db.commit()
    return db_signature
