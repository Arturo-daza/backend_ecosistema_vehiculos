from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from services.file import FileService
from utils.jwt_manager import create_token, validate_token
from services.user import UserService
from config.database import Database 
from schemas.user import UserCreate, User
from schemas.auth import RecoverPasswordRequest, ResetPasswordRequest
from utils.email_sender import send_recovery_email
from passlib.context import CryptContext



auth_router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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
    
    if user.FotoPerfil is not None:
        file_service = FileService(db)
        file = file_service.get_file(user.FotoPerfil)
        if file is not None:
            user.FotoPerfil = file.Ruta  # Añadir la URL de la foto al JSON
        else:
            user.FotoPerfil = None
    else:
        user.FotoPerfil= None  # Si no tiene foto, devolver null o algo equivalente

    # Crear token con los datos del usuario
    token = create_token(data={"id": user.IdUsuario, "email": user.Email, "nombre": user.Nombre, "documento": user.NumeroDocumento, "telefono": user.Telefono, "foto_perfil": user.FotoPerfil, "active": user.Activo,   "tipo_usuario": user.TipoUsuario, "role": user.IdRol})

    return {"access_token": token, "token_type": "bearer"}

@auth_router.post("/register", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user_service = UserService(db)
    return user_service.create_user(user=user)


@auth_router.post("/recover-password")
def recover_password(recover_request: RecoverPasswordRequest, db: Session = Depends(get_db)):
    user_service = UserService(db)
    user = user_service.get_user_by_email(recover_request.email)
    
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Generar token de recuperación
    recovery_token = create_token({"email": user.Email})
    
    # Opcional: Guarda el token en la base de datos si no estás usando JWT o quieres persistencia.
    
    # Enviar el email de recuperación con el token
    recovery_link = f"http://ecosistemadigital.site/reset-password?token={recovery_token}"
    send_recovery_email(user.Email, recovery_link)

    return {"message": "Se ha enviado un enlace de recuperación a tu correo."}

@auth_router.post("/reset-password")
def reset_password(reset_request: ResetPasswordRequest, db: Session = Depends(get_db)):
    token = reset_request.token
    new_password = reset_request.new_password

    # Validar el token y obtener el email del token
    try:
        token_data = validate_token(token)
    except:
        raise HTTPException(status_code=400, detail="Token inválido o expirado")

    email = token_data.get("email")
    if not email:
        raise HTTPException(status_code=400, detail="Token inválido")

    # Obtener al usuario por su email
    user_service = UserService(db)
    user = user_service.get_user_by_email(email)
    
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Hashear la nueva contraseña
    hashed_password = pwd_context.hash(new_password)

    # Actualizar la contraseña del usuario
    user.Contrasena = hashed_password
    db.commit()

    return {"message": "Contraseña restablecida exitosamente"}