from sqlalchemy.orm import Session
from models import ActivityLog
from schemas.activity_logs import ActivityLogCreate

def create_activity_log(db: Session, log: ActivityLogCreate):
    """Guarda un evento en el registro de actividades."""
    db_log = ActivityLog(
        user_id=log.user_id,
        action=log.action
    )
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

def get_activity_logs(db: Session, skip: int = 0, limit: int = 10):
    """Obtiene el historial de eventos del sistema."""
    return db.query(ActivityLog).order_by(ActivityLog.timestamp.desc()).offset(skip).limit(limit).all()
