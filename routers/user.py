from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from schemas.user import UserUpdate, User
from config.database import Database
from sqlalchemy.orm import Session
from services.user import UserService
from schemas.user import User
from middlewares.jwt_bearer import JWTBearer
from fastapi.security import OAuth2PasswordBearer
from utils.jwt_manager import validate_token
from fastapi import HTTPException, status

# Usamos JWTBearer para verificar el token en rutas protegidas
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

user_router = APIRouter()

database = Database.get_instance()
get_db = database.get_db



@user_router.get("/me",response_model=User,  dependencies=[Depends(JWTBearer())])
def read_users_me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Ruta protegida que devuelve información del usuario autenticado.
    """
    user_service = UserService(db)
    data= validate_token(token)
    return user_service.get_user_by_email(data['email'])

# Actualizar un usuario
@user_router.put("/update", response_model=User, status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())])
def update_user_route(user: UserUpdate, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user_service = UserService(db)
    data = validate_token(token)  # Validar el token para obtener información del usuario
    user_id = data['id']  # Asegúrate de que el token contenga el user_id
    updated_user = user_service.update_user(user_id, user)
    if not updated_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    return updated_user


# Eliminar un usuario
@user_router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(JWTBearer())])
def delete_user_route(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user_service = UserService(db)
    data = validate_token(token)  # Validar el token para obtener información del usuario
    user_id = data['id']  # Asegúrate de que el token contenga el user_id
    deleted = user_service.delete_user(user_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    return {"message": "Usuario eliminado"}

# # Obtener un usuario por ID
# @user_router.get("/{user_id}", response_model=User, status_code=status.HTTP_200_OK)
# async def get_user_route(user_id: int, db: Session = Depends(get_db), user_service: UserService = Depends(UserService)):
#     user = user_service.get_user(user_id)
#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
#     return user

# # Crear un nuevo usuario
# @user_router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
# async def create_user_route(user: UserCreate, db: Session = Depends(get_db), user_service: UserService = Depends(UserService)):
#     new_user = user_service.create_user(user)
#     return new_user

