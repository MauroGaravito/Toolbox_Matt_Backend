from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import HTTPException
from models import DigitalSignature, Signature, User
from schemas.digital_signatures import DigitalSignatureCreate

def create_signature(db: Session, user: User, signature_data: DigitalSignatureCreate):
    print("👉 Entrando a create_signature (desde CRUD)")
    print("🧾 Datos recibidos:", signature_data.dict())

    # 🔒 Validar si ya existe una firma con ese email para ese Toolbox Talk
    existing_signature = db.query(Signature).filter(
        Signature.toolbox_talk_id == signature_data.toolbox_talk_id,
        Signature.signer_email == signature_data.email
    ).first()

    if existing_signature:
        raise HTTPException(status_code=400, detail="This email has already signed this Toolbox Talk.")

    # 🟢 Guardar en digital_signatures
    digital_sig = DigitalSignature(
        user_id=user.id,
        toolbox_talk_id=signature_data.toolbox_talk_id,
        full_name=signature_data.full_name,
        email=signature_data.email,
        signed_at=datetime.utcnow()
    )
    db.add(digital_sig)
    db.commit()
    db.refresh(digital_sig)

    # ✒️ Guardar en signatures si hay imagen
    if signature_data.signature_image:
        print("✅ Imagen recibida, guardando en tabla Signature")
        signature = Signature(
            toolbox_talk_id=signature_data.toolbox_talk_id,
            signer_name=signature_data.full_name,
            signer_email=signature_data.email,
            signature_image=signature_data.signature_image,
            signed_at=datetime.utcnow()
        )
        db.add(signature)
        db.commit()
        db.refresh(signature)
    else:
        print("⚠️ No se recibió imagen de firma")

    return digital_sig

def get_signatures_by_toolbox_talk(db: Session, toolbox_talk_id: int):
    return db.query(DigitalSignature).filter(DigitalSignature.toolbox_talk_id == toolbox_talk_id).all()
