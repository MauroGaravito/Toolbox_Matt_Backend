import os
from dotenv import load_dotenv

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# ✅ Carga variables de entorno
load_dotenv()

# ✅ Importa routers (sin backend.)
from routers import (
    auth,
    reference_documents,
    signatures,
    digital_signatures,
    activity_logs,
    toolbox_talks,
    users,
)

# ✅ Modelos y base de datos
import models
import database

# ✅ Instancia de FastAPI
app = FastAPI()

# ✅ Middleware para forzar HTTPS en el panel admin (solo en producción)
if os.getenv("ENV") == "production":
    from middleware.force_https_admin import ForceHttpsAdminFormMiddleware
    app.add_middleware(ForceHttpsAdminFormMiddleware)

# ✅ CORS
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost",
    "http://127.0.0.1",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://toolbox.downundersolutions.com",
    "https://toolboxmattfrontend-production.up.railway.app",
    "https://toolbox-matt-frontend.onrender.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Panel Admin
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
