from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from jwt_manager import create_token
from services.user import UserService
from config.database import Database  # Asumo que tienes una función para obtener la sesión de la DB



auth_router = APIRouter()

database = Database.get_instance()
get_db = database.get_db

@auth_router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Login del usuario, validando el email y la contraseña.
    """
    print(form_data.username)
    user_service = UserService(db)
    user = user_service.get_user_by_email(form_data.username)

    if user is None or not user_service.verify_password(form_data.password, user.Contrasena):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    # Crear token con los datos del usuario
    token = create_token(data={"id": user.IdUsuario, "email": user.Email,  "tipo_usuario": user.TipoUsuario, "role": user.IdRol})

    return {"access_token": token, "token_type": "bearer"}
