import os
import sys
from dotenv import load_dotenv

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# ✅ Cambiar el sys.path para incluir el directorio de backend dentro del contenedor
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend'))

# ✅ Carga variables de entorno
load_dotenv()

# ✅ Routers
from routers import (
    auth,
    reference_documents,
    signatures,
    digital_signatures,
    activity_logs,
    toolbox_talks,
    users,
)

# ✅ Panel admin
from admin import setup_admin
import models

# ✅ Instancia FastAPI
app = FastAPI()

# ✅ Orígenes permitidos (dev + producción)
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost",
    "http://127.0.0.1",
    "http://localhost:3000",          # 👈 necesario
    "http://127.0.0.1:3000",          # 👈 necesario
    "https://toolbox.downundersolutions.com",
]


# ✅ Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex=r"https://.*\.netlify\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Setup SQLAdmin
setup_admin(app)

# ✅ Routers
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
