import openai
import pdfplumber
from docx import Document
import requests
import os
from dotenv import load_dotenv
from openai import OpenAI
import faiss
import pickle

# Cargar las variables de entorno
load_dotenv()

# Asume que tienes tu clave API de OpenAI aquí
openai.api_key = os.getenv("OPENAI_API_KEY")


# Obtener las credenciales de Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

def extract_text_from_pdf(pdf_path):
    """
    Extrae texto de un archivo PDF usando pdfplumber.
    """
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text

def extract_text_from_docx(docx_path):
    """
    Extrae texto de un archivo DOCX usando python-docx.
    """
    doc = Document(docx_path)
    text = ""
    for para in doc.paragraphs:
        text += para.text
    return text


client = OpenAI()

def generate_embeddings(text: str):
    text = truncate_text_to_token_limit(text)
    response = client.embeddings.create(
        model="text-embedding-ada-002",
        input=text
    )
    return response.data[0].embedding



def upload_to_supabase(file_name):
    """
    Subir el archivo FAISS (.index) al bucket de Supabase Storage.
    """
    # Ruta local del archivo en tu proyecto
    local_path = os.path.join("backend", "faiss_indexes", file_name)

    # Supabase URL destino
    url = f"{SUPABASE_URL}/storage/v1/object/toolbox-indexes/{file_name}"

    SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

    headers = {
        "Authorization": f"Bearer {SUPABASE_SERVICE_ROLE_KEY}",
        "Content-Type": "application/octet-stream"
    }


    print(f"Subiendo archivo {local_path} a Supabase...")

    # Abrir el archivo FAISS .index para subirlo
    try:
        with open(local_path, "rb") as file:
            response = requests.put(url, headers=headers, data=file)  # PUT directo

        if response.status_code == 200:
            print(f"✅ Archivo {file_name} subido exitosamente a Supabase.")
        else:
            print(f"❌ Error al subir el archivo {file_name}: {response.text}")
            print(f"Response code: {response.status_code}")
            print(f"Response content: {response.content}")
    except Exception as e:
        print(f"❌ Error al intentar abrir el archivo {local_path}: {str(e)}")



def truncate_text_to_token_limit(text: str, max_tokens: int = 8192) -> str:
    approx_tokens_per_word = 1.5
    max_words = int(max_tokens / approx_tokens_per_word)
    words = text.split()

    if len(words) > max_words:
        print(f"⚠️ Texto demasiado largo ({len(words)} palabras). Se truncará a {max_words} palabras (~{max_tokens} tokens).")
        words = words[:max_words]

    return " ".join(words)

import numpy as np  # asegurate de tener esta línea al inicio del archivo

def query_faiss_index(index_name: str, query_embedding: list[float], top_k: int = 5):
    """
    Carga el índice FAISS guardado y devuelve los fragmentos más relevantes.
    """
    index_path = os.path.join("backend", "faiss_indexes", index_name)

    if not os.path.exists(index_path):
        raise FileNotFoundError(f"Index file {index_path} not found.")

    # Cargar índice
    index = faiss.read_index(index_path)

    # Cargar metadatos de fragmentos
    metadata_path = index_path.replace(".index", ".pkl")
    with open(metadata_path, "rb") as f:
        fragments = pickle.load(f)

    # Convertir embedding a np.array con forma correcta (1, D)
    query_vector = np.array([query_embedding]).astype("float32")

    # Buscar los fragmentos más cercanos
    D, I = index.search(query_vector, top_k)
    matched_fragments = [fragments[i] for i in I[0] if i < len(fragments)]

    return matched_fragments
