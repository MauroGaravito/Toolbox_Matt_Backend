import os
import sys
from dotenv import load_dotenv

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from middleware.force_https_admin import ForceHttpsAdminFormMiddleware

# ✅ Agrega el path al backend para que se pueda importar desde cualquier punto
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend'))

# ✅ Carga variables de entorno desde .env
load_dotenv()

# ✅ Importa routers y configuración
from routers import (
    auth,
    reference_documents,
    signatures,
    digital_signatures,
    activity_logs,
    toolbox_talks,
    users,
)

from admin import setup_admin
import models

# ✅ Instancia principal de FastAPI
app = FastAPI()

# ✅ Middleware para corregir Mixed Content en /admin/login
app.add_middleware(ForceHttpsAdminFormMiddleware)

# ✅ CORS: permite que el frontend se comunique con el backend
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost",
    "http://127.0.0.1",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://toolbox.downundersolutions.com",
    "https://toolboxmattbackend-production.up.railway.app/",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex=r"https://.*\.netlify\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Admin panel con SQLAdmin
setup_admin(app)

# ✅ Registro de rutas de la API
app.include_router(auth.router)
app.include_router(toolbox_talks.router)
app.include_router(reference_documents.router)
app.include_router(signatures.router)
app.include_router(digital_signatures.router)
app.include_router(activity_logs.router)
app.include_router(users.router)

# ✅ Ruta básica de prueba
@app.get("/ping")
def ping():
    return {"message": "pong"}
