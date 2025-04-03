import faiss
import numpy as np
from models import ReferenceDocument, GeneratedToolboxTalk
from utils import (
    extract_text_from_pdf,
    extract_text_from_docx,
    generate_embeddings,
    upload_to_supabase,
)
from fastapi import HTTPException
from sqlalchemy.orm import Session
import os
import pickle

def create_faiss_index(db: Session, toolbox_talk_id: int, document_ids: list[int]):
    print("📥 GENERANDO FAISS INDEX PARA:")
    print("🧱 ToolboxTalk ID:", toolbox_talk_id)
    print("📎 Document IDs:", document_ids)

    # 🔍 Validar existencia del Toolbox Talk
    toolbox_talk = db.query(GeneratedToolboxTalk).filter(GeneratedToolboxTalk.id == toolbox_talk_id).first()
    if not toolbox_talk:
        raise HTTPException(status_code=404, detail="Toolbox Talk not found")

    # 📂 Buscar los documentos seleccionados por ID
    documents = db.query(ReferenceDocument).filter(ReferenceDocument.id.in_(document_ids)).all()
    if not documents:
        raise HTTPException(status_code=404, detail="No documents found for this Toolbox Talk")

    embeddings = []
    fragments = []  # 🧩 Guardaremos los textos para el .pkl

    for doc in documents:
        try:
            if doc.file_path.endswith(".pdf"):
                text = extract_text_from_pdf(doc.file_path)
            elif doc.file_path.endswith(".docx"):
                text = extract_text_from_docx(doc.file_path)
            else:
                raise ValueError(f"Unsupported file type: {doc.file_name}")

            if not text.strip():
                raise ValueError(f"No text extracted from: {doc.file_name}")

            embedding = generate_embeddings(text)
            embeddings.append(embedding)
            fragments.append(text)  # 🧠 Guardar el texto completo como fragmento

        except Exception as e:
            print("❌ Error al generar índice:", e)
            raise HTTPException(status_code=500, detail=f"Error generating index: {str(e)}")

    if not embeddings:
        raise HTTPException(status_code=400, detail="No embeddings generated from documents.")

    # 🧠 Crear índice FAISS
    dim = len(embeddings[0])
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings).astype("float32"))

    # 💾 Guardar archivo local antes de subirlo a Supabase
    file_name = f"toolbox_talk_{toolbox_talk_id}.index"
    index_path = os.path.join("backend", "faiss_indexes", file_name)
    os.makedirs(os.path.dirname(index_path), exist_ok=True)

    faiss.write_index(index, index_path)

    # 💾 Guardar también el archivo .pkl con los fragmentos
    metadata_path = index_path.replace(".index", ".pkl")
    with open(metadata_path, "wb") as f:
        pickle.dump(fragments, f)

    # ☁️ Subir archivo .index a Supabase
    upload_to_supabase(file_name)

    # 🔗 Asociar el índice con el Toolbox Talk
    toolbox_talk.index_file = file_name
    db.commit()

    return {"message": "FAISS index created and uploaded successfully."}

