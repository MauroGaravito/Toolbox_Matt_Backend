from sqlalchemy.orm import Session
from models import GeneratedToolboxTalk
from schemas.toolbox_talks import ToolboxTalkCreate, ToolboxTalkUpdate
from fastapi import APIRouter
import os
from database import get_db
from models import GeneratedToolboxTalk, User, ToolboxTalkParticipant

router = APIRouter()


def create_toolbox_talk(db: Session, toolbox_talk: ToolboxTalkCreate):
    """Crea un nuevo Toolbox Talk generado por IA."""
    db_toolbox_talk = GeneratedToolboxTalk(
        topic=toolbox_talk.topic,
        content=toolbox_talk.content,
        created_by=toolbox_talk.created_by
    )
    db.add(db_toolbox_talk)
    db.commit()
    db.refresh(db_toolbox_talk)
    return db_toolbox_talk

def get_toolbox_talk(db: Session, toolbox_talk_id: int):
    """Obtiene un Toolbox Talk específico."""
    return db.query(GeneratedToolboxTalk).filter(GeneratedToolboxTalk.id == toolbox_talk_id).first()

def update_toolbox_talk(db: Session, toolbox_talk_id: int, toolbox_talk_update: ToolboxTalkUpdate):
    """Actualiza un Toolbox Talk existente."""
    db_toolbox_talk = db.query(GeneratedToolboxTalk).filter(GeneratedToolboxTalk.id == toolbox_talk_id).first()
    if not db_toolbox_talk:
        return None

    db_toolbox_talk.topic = toolbox_talk_update.topic or db_toolbox_talk.topic
    db_toolbox_talk.content = toolbox_talk_update.content or db_toolbox_talk.content
    db.commit()
    db.refresh(db_toolbox_talk)
    return db_toolbox_talk

def delete_toolbox_talk(db: Session, toolbox_talk_id: int):
    """Elimina un Toolbox Talk."""
    db_toolbox_talk = db.query(GeneratedToolboxTalk).filter(GeneratedToolboxTalk.id == toolbox_talk_id).first()
    if db_toolbox_talk:
        db.delete(db_toolbox_talk)
        db.commit()
    return db_toolbox_talk

def generate_content_for_toolbox_talk(db: Session, toolbox_talk_id: int, generated_text: str):
    talk = db.query(GeneratedToolboxTalk).filter(GeneratedToolboxTalk.id == toolbox_talk_id).first()
    if not talk:
        return None
    talk.content = generated_text
    db.commit()
    db.refresh(talk)
    return talk

def get_all_toolbox_talks(db: Session):
    return db.query(GeneratedToolboxTalk).order_by(GeneratedToolboxTalk.created_at.desc()).all()

def get_toolbox_talks_by_user(db: Session, user_id: int):
    return db.query(GeneratedToolboxTalk).filter_by(created_by=user_id).order_by(GeneratedToolboxTalk.created_at.desc()).all()

def assign_user_to_toolbox_talk(db: Session, talk_id: int, user_id: int):
    """Asigna un usuario existente a un Toolbox Talk (admin only)"""
    existing = db.query(ToolboxTalkParticipant).filter_by(toolbox_talk_id=talk_id, user_id=user_id).first()
    if existing:
        raise ValueError("User already assigned")

    participant = ToolboxTalkParticipant(toolbox_talk_id=talk_id, user_id=user_id)
    db.add(participant)
    db.commit()
    db.refresh(participant)
    return participant

def get_participants_by_talk(db: Session, talk_id: int):
    """Devuelve todos los participantes asignados a un Toolbox Talk"""
    return db.query(ToolboxTalkParticipant).filter_by(toolbox_talk_id=talk_id).all()

def unassign_user_from_talk(db: Session, talk_id: int, user_id: int):
    participant = db.query(ToolboxTalkParticipant).filter_by(
        toolbox_talk_id=talk_id, user_id=user_id
    ).first()
    if not participant:
        return None
    db.delete(participant)
    db.commit()
    return participant
