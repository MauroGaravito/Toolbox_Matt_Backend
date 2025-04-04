import os
import sys
from dotenv import load_dotenv

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# ✅ Corrige path si backend está en subcarpeta
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend'))

# ✅ Carga las variables de entorno
load_dotenv()

# ✅ Importa routers primero (no causa problemas)
from routers import (
    auth,
    reference_documents,
    signatures,
    digital_signatures,
    activity_logs,
    toolbox_talks,
    users,
)

# ✅ Modelos de BD (asegura que estén inicializados antes del admin)
import models

# ✅ Instancia de FastAPI
app = FastAPI()

# ✅ Middleware para forzar HTTPS en formulario del admin
from middleware.force_https_admin import ForceHttpsAdminFormMiddleware
app.add_middleware(ForceHttpsAdminFormMiddleware)

# ✅ Configuración CORS
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost",
    "http://127.0.0.1",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://toolbox.downundersolutions.com",
    "https://toolboxmattfrontend-production.up.railway.app",  # 👈 agrega esto
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex=r"https://.*\.netlify\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Importa y registra el panel admin después de crear `app`
from admin import setup_admin
setup_admin(app)

# ✅ Registro de rutas
app.include_router(auth.router)
app.include_router(toolbox_talks.router)
app.include_router(reference_documents.router)
app.include_router(signatures.router)
app.include_router(digital_signatures.router)
app.include_router(activity_logs.router)
app.include_router(users.router)

# ✅ Ruta de prueba
@app.get("/ping")
def ping():
    return {"message": "pong"}
