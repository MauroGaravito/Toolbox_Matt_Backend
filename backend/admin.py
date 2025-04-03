from sqladmin import Admin, ModelView
from sqladmin.authentication import AuthenticationBackend
from fastapi import Request
from sqlalchemy.orm import Session
from database import engine, SessionLocal
from models import User, RoleEnum
from security import verify_password, hash_password
import jwt
import os
from wtforms import Form, StringField, PasswordField, SelectField
from wtforms.validators import DataRequired, Email

# Configuración de autenticación con JWT
SECRET_KEY = os.getenv("SECRET_KEY", "super_secretkey")
ALGORITHM = "HS256"

# Formulario personalizado para el admin
class UserForm(Form):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    role = SelectField("Role", choices=[("admin", "admin"), ("worker", "worker")])
    password = PasswordField("Password")  # Campo virtual

# Backend de autenticación para SQLAdmin
class AdminAuth(AuthenticationBackend):
    def __init__(self, secret_key: str):
        super().__init__(secret_key=secret_key)
        self.secret_key = secret_key

    async def login(self, request: Request) -> bool:
        form = await request.form()
        username = form["username"]
        password = form["password"]

        db: Session = SessionLocal()
        user = db.query(User).filter(User.username == username).first()
        db.close()

        if not user or not verify_password(str(password), str(user.hashed_password)):
            return False

        token = jwt.encode({"sub": user.username}, self.secret_key, algorithm=ALGORITHM)
        request.session.update({"token": token})
        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")
        if not token:
            return False
        try:
            jwt.decode(token, self.secret_key, algorithms=[ALGORITHM])
            return True
        except jwt.PyJWTError:
            return False

auth_backend = AdminAuth(secret_key=SECRET_KEY)

# Vista de administración para el modelo User
class UserAdmin(ModelView, model=User):
    form_class = UserForm

    column_list = ["id", "username", "email", "role", "created_at"]
    column_labels = {
        "id": "ID",
        "username": "Username",
        "email": "Email",
        "role": "Role",
        "created_at": "Created At"
    }

    column_searchable_list = [User.username.name, User.email.name, User.role.name]
    column_sortable_list = ["id", "username", "created_at"]

    form_excluded_columns = [
        "id",
        "created_at",
        "hashed_password",
        "generated_toolbox_talks",
        "activities"
    ]


    can_create = True
    can_edit = True
    can_delete = True

    def is_accessible(self, request: Request) -> bool:
        token = request.session.get("token")
        if not token:
            return False
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if not username:
                return False

            db = SessionLocal()
            user = db.query(User).filter(User.username == username).first()
            db.close()

            return user and user.role == RoleEnum.admin
        except Exception:
            return False

    async def insert_model(self, request: Request, data: dict):
        if data.get("password"):
            data["hashed_password"] = hash_password(data["password"])
        data.pop("password", None)
        return await super().insert_model(request, data)

    async def update_model(self, request: Request, pk: str, data: dict):
        if data.get("password"):
            data["hashed_password"] = hash_password(data["password"])
        data.pop("password", None)
        return await super().update_model(request, pk, data)

# ✅ Registrar el panel de administración correctamente
def setup_admin(app):
    admin = Admin(
        app,
        engine,
        authentication_backend=auth_backend,
        base_url="/admin"  # <- IMPORTANTE: debe comenzar con "/"
    )
    admin.add_view(UserAdmin)
