from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas.toolbox_talks import ToolboxTalkCreate, ToolboxTalkUpdate, ToolboxTalkResponse
from crud.toolbox_talks import create_toolbox_talk, get_toolbox_talk, update_toolbox_talk, delete_toolbox_talk, get_participants_by_talk
from typing import List
from openai import OpenAI
from crud.toolbox_talks import generate_content_for_toolbox_talk
import os
from fastapi import Body
from crud.faiss import create_faiss_index
from security import get_current_user
from crud.toolbox_talks import get_all_toolbox_talks, get_toolbox_talks_by_user
from models import User, RoleEnum, ToolboxTalkParticipant, GeneratedToolboxTalk
from schemas.participants import ParticipantResponse
from pydantic import BaseModel

# Define the Pydantic model for the document ID list
class DocumentIDList(BaseModel):
    document_ids: List[int]

router = APIRouter(
    prefix="/toolbox-talks",
    tags=["Generated Toolbox Talks"]
)

@router.post("/", response_model=ToolboxTalkResponse)
def create_new_toolbox_talk(
    toolbox_talk: ToolboxTalkCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role not in [RoleEnum.admin, RoleEnum.supervisor]:
        raise HTTPException(status_code=403, detail="Not authorized to create toolbox talks")
    return create_toolbox_talk(db, toolbox_talk)

@router.get("/", response_model=List[ToolboxTalkResponse])
def list_toolbox_talks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role == "admin":
        return get_all_toolbox_talks(db)
    return get_toolbox_talks_by_user(db, user_id=current_user.id)

@router.get("/{toolbox_talk_id}", response_model=ToolboxTalkResponse)
def read_toolbox_talk(toolbox_talk_id: int, db: Session = Depends(get_db)):
    db_toolbox_talk = get_toolbox_talk(db, toolbox_talk_id)
    if not db_toolbox_talk:
        raise HTTPException(status_code=404, detail="Toolbox Talk not found")
    return db_toolbox_talk

@router.put("/{toolbox_talk_id}", response_model=ToolboxTalkResponse)
def update_existing_toolbox_talk(toolbox_talk_id: int, toolbox_talk_update: ToolboxTalkUpdate, db: Session = Depends(get_db)):
    db_toolbox_talk = update_toolbox_talk(db, toolbox_talk_id, toolbox_talk_update)
    if not db_toolbox_talk:
        raise HTTPException(status_code=404, detail="Toolbox Talk not found")
    return db_toolbox_talk

@router.delete("/{toolbox_talk_id}", response_model=ToolboxTalkResponse)
def delete_existing_toolbox_talk(toolbox_talk_id: int, db: Session = Depends(get_db)):
    db_toolbox_talk = delete_toolbox_talk(db, toolbox_talk_id)
    if not db_toolbox_talk:
        raise HTTPException(status_code=404, detail="Toolbox Talk not found")
    return db_toolbox_talk

@router.post("/{toolbox_talk_id}/generate-index")
def generate_index_for_toolbox_talk(
    toolbox_talk_id: int,
    payload: DocumentIDList,  # Use the new Pydantic model here
    db: Session = Depends(get_db)
):
    if not payload.document_ids:
        raise HTTPException(status_code=400, detail="No document IDs provided")

    try:
        result = create_faiss_index(db, toolbox_talk_id, payload.document_ids)
        return {"message": "Index generated successfully", "faiss_file": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating index: {str(e)}")

@router.post("/{talk_id}/generate-with-context")
def generate_with_context(
    talk_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    talk = db.query(GeneratedToolboxTalk).filter(GeneratedToolboxTalk.id == talk_id).first()
    if not talk:
        raise HTTPException(status_code=404, detail="Toolbox Talk not found")

    index_name = f"toolbox_talk_{talk_id}.index"
    index_path = os.path.abspath(os.path.join("backend", "faiss_indexes", index_name))
    print("🧪 Ruta absoluta del FAISS index:", index_path)

    # 1. Si no hay documentos subidos:
    if not talk.documents:
        prompt = f"Generate a professional Toolbox Talk for the topic: '{talk.topic}'. Include introduction, hazards, controls, discussion points, and conclusion."
        print("⚠️ No documents found, generating general content.")
        return _generate_and_save(db, talk, prompt)

    # 2. Si hay documentos pero NO hay index
    if not os.path.exists(index_path):
        print("❌ No se encontró el archivo FAISS index.")
        raise HTTPException(status_code=400, detail="Documents found but index not generated yet.")

    # 3. Si hay index: hacemos búsqueda
    from utils import generate_embeddings, query_faiss_index

    query_embedding = generate_embeddings(talk.topic)
    # Limitar a top_k fragmentos (por defecto 5)
    fragments = query_faiss_index(index_name, query_embedding, top_k=5)
    # Truncar cada fragmento a 1500 caracteres
    context = "\n\n".join(fragment[:1500] for fragment in fragments)
    prompt = (
        f"Based on the following reference material:\n\n{context}\n\n"
        f"Generate a formal, written Toolbox Talk document for the topic: '{talk.topic}'. "
        "The document should include: Introduction, Hazards, Risk Controls, Discussion Points, and Conclusion. "
        "Do not include phrases like 'Good morning' or 'Let’s talk about'. "
        "Write in a formal, impersonal tone suitable for printed distribution as an official WHS reference document. "
        "Clearly mention that the content is based on the supplied document(s), such as the Model Code of Practice – Construction Work (November 2024), or other relevant codes."
    )

    return _generate_and_save(db, talk, prompt)

def _generate_and_save(db, talk, prompt: str):
    from openai import OpenAI
    import os

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a WHS advisor in Australia. Your job is to generate professional, structured Toolbox Talks based on Australian Codes of Practice. These documents are meant to be read, not presented aloud, and must serve as written reference materials. The output must be clear, formal, objective, and aligned with Safe Work Australia standards."
                    "You generate complete, professional Toolbox Talks in accordance with the Safe Work Australia Code of Practice. "
                    "Your answers include detailed sections such as: Introduction, Hazards, Risk Controls, Discussion Points, and Conclusion. "
                    "Make sure the Toolbox Talk is clear, practical, and long enough to be used in a real-life briefing session."
                )
            },
            {
                "role": "user",
                "content": prompt + " Expand each section with practical examples and WHS-aligned explanations to ensure clarity and completeness."
            }
        ],
        temperature=0.7,
        max_tokens=2048
    )


    generated = response.choices[0].message.content
    talk.content = generated
    db.commit()
    return {"content": generated}

@router.post("/{talk_id}/assign-user/{user_id}")
def assign_user_to_talk(
    talk_id: int,
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != RoleEnum.admin:
        raise HTTPException(status_code=403, detail="Only admins can assign users")

    # Validaciones
    user = db.query(User).filter(User.id == user_id).first()
    talk = db.query(GeneratedToolboxTalk).filter(GeneratedToolboxTalk.id == talk_id).first()
    if not user or not talk:
        raise HTTPException(status_code=404, detail="User or Toolbox Talk not found")

    # Evitar duplicados
    existing = db.query(ToolboxTalkParticipant).filter_by(toolbox_talk_id=talk_id, user_id=user_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="User already assigned")

    participant = ToolboxTalkParticipant(toolbox_talk_id=talk_id, user_id=user_id)
    db.add(participant)
    db.commit()
    return {"message": f"User {user.email} assigned to Toolbox Talk {talk.topic}"}

@router.get("/{talk_id}/participants", response_model=List[ParticipantResponse])
def list_participants_for_talk(
    talk_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    talk = db.query(GeneratedToolboxTalk).filter_by(id=talk_id).first()
    if not talk:
        raise HTTPException(status_code=404, detail="Toolbox Talk not found")

    return get_participants_by_talk(db, talk_id)

@router.delete("/{talk_id}/unassign-user/{user_id}")
def unassign_user_from_talk(
    talk_id: int,
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != RoleEnum.admin:
        raise HTTPException(status_code=403, detail="Only admins can unassign users")

    participant = db.query(ToolboxTalkParticipant).filter_by(
        toolbox_talk_id=talk_id,
        user_id=user_id
    ).first()

    if not participant:
        raise HTTPException(status_code=404, detail="User is not assigned to this talk")

    db.delete(participant)
    db.commit()
    return {"message": f"User {user_id} unassigned from Toolbox Talk {talk_id}"}
