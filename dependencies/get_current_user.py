from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from services.user import UserService
from utils.jwt_manager import validate_token
from config.database import Database

database = Database.get_instance()
get_db = database.get_db


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")  # Asegúrate de que esta URL coincida con tu ruta de inicio de sesión

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    # Validar el token y obtener los datos del usuario
    try:
        payload = validate_token(token)
        email = payload.get("email")  # Cambia esto si usas otro campo
        if email is None:
            raise HTTPException(status_code=401, detail="Token inválido")
    except Exception:
        raise HTTPException(status_code=401, detail="Token inválido")

    # Obtener el usuario de la base de datos
    user_service = UserService(db)
    user = user_service.get_user_by_email(email)
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return user
