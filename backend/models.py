from sqlalchemy import Column, Integer, String, Enum, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from database import Base
import enum
from datetime import datetime

# 🎭 Enum para los roles de usuario
class RoleEnum(enum.Enum):
    admin = "admin"
    supervisor = "supervisor"
    worker = "worker"

# 🟢 Tabla de Usuarios
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(Enum(RoleEnum), default=RoleEnum.worker)
    created_at = Column(DateTime, default=datetime.utcnow)

    generated_toolbox_talks = relationship("GeneratedToolboxTalk", back_populates="creator")
    activities = relationship("ActivityLog", back_populates="user")
    digital_signatures = relationship("DigitalSignature", back_populates="user")

# 🟡 Tabla de Toolbox Talks Generados (por la IA)
class GeneratedToolboxTalk(Base):
    __tablename__ = "generated_toolbox_talks"

    id = Column(Integer, primary_key=True, index=True)
    topic = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    creator = relationship("User", back_populates="generated_toolbox_talks")
    signatures = relationship("Signature", back_populates="toolbox_talk", cascade="all, delete")
    documents = relationship("ReferenceDocument", back_populates="toolbox_talk", cascade="all, delete")
    digital_signatures = relationship("DigitalSignature", back_populates="toolbox_talk", cascade="all, delete")
    participants = relationship("ToolboxTalkParticipant", back_populates="toolbox_talk", cascade="all, delete")
    vector_indexes = relationship("VectorIndex", back_populates="toolbox_talk", cascade="all, delete")

# 🟠 Tabla de Documentos de Referencia
class ReferenceDocument(Base):
    __tablename__ = "reference_documents"

    id = Column(Integer, primary_key=True, index=True)
    uploaded_by = Column(Integer, ForeignKey("users.id"))
    file_name = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)

    toolbox_talk_id = Column(Integer, ForeignKey("generated_toolbox_talks.id"), nullable=True)
    toolbox_talk = relationship("GeneratedToolboxTalk", back_populates="documents")

# 🟣 Tabla de Firmas con Imagen
class Signature(Base):
    __tablename__ = "signatures"

    id = Column(Integer, primary_key=True, index=True)
    toolbox_talk_id = Column(Integer, ForeignKey("generated_toolbox_talks.id"))
    signer_name = Column(String, nullable=False)
    signer_email = Column(String, nullable=True)
    signature_image = Column(Text, nullable=True)
    signed_at = Column(DateTime, default=datetime.utcnow)

    toolbox_talk = relationship("GeneratedToolboxTalk", back_populates="signatures")

# 🔵 Tabla de Registro de Actividad
class ActivityLog(Base):
    __tablename__ = "activity_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    action = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="activities")

# 🔴 Tabla de Firmas Digitales
class DigitalSignature(Base):
    __tablename__ = "digital_signatures"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    toolbox_talk_id = Column(Integer, ForeignKey("generated_toolbox_talks.id"), nullable=False)
    full_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    signed_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="digital_signatures")
    toolbox_talk = relationship("GeneratedToolboxTalk", back_populates="digital_signatures")

# Tabla de Participantes de Toolbox Talk
class ToolboxTalkParticipant(Base):
    __tablename__ = "toolbox_talk_participants"

    id = Column(Integer, primary_key=True, index=True)
    toolbox_talk_id = Column(Integer, ForeignKey("generated_toolbox_talks.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    assigned_at = Column(DateTime, default=datetime.utcnow)

    toolbox_talk = relationship("GeneratedToolboxTalk", back_populates="participants")
    user = relationship("User")

# 🧠 Tabla para almacenar información de FAISS en la base de datos
class VectorIndex(Base):
    __tablename__ = "vector_indexes"

    id = Column(Integer, primary_key=True, index=True)
    toolbox_talk_id = Column(Integer, ForeignKey("generated_toolbox_talks.id"), nullable=False)
    file_path_index = Column(String, nullable=False)
    file_path_metadata = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    toolbox_talk = relationship("GeneratedToolboxTalk", back_populates="vector_indexes")

# 📄 Tabla para almacenar fragmentos de texto procesados de cada documento
class DocumentFragment(Base):
    __tablename__ = "document_fragments"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("reference_documents.id"), nullable=False)
    toolbox_talk_id = Column(Integer, ForeignKey("generated_toolbox_talks.id"), nullable=False)
    content = Column(Text, nullable=False)
    embedding = Column(Text, nullable=True)  # O usa LargeBinary si guardas el array como binario
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relaciones
    document = relationship("ReferenceDocument", backref="fragments")
    toolbox_talk = relationship("GeneratedToolboxTalk", backref="fragments")
