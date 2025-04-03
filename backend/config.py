import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env en el mismo directorio
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)

# 🔐 Seguridad JWT
SECRET_KEY = os.getenv("SECRET_KEY", "secret_key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

# 🛢️ Base de datos
DATABASE_URL = os.getenv("DATABASE_URL")

# 🔍 Modo (opcional: para diferenciar entre dev y prod)
ENV = os.getenv("ENV", "development")  # o "production"

# ✅ DEBUG opcional (solo si estás testeando)
if ENV == "development":
    print(f"✅ .env cargado correctamente desde: {dotenv_path}")
    print(f"✅ DATABASE_URL: {DATABASE_URL}")
        
