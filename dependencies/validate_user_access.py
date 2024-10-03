from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from models.user import User as UserModel
from dependencies.get_db import get_db
from dependencies.get_current_user import get_current_user


def validate_user_access(user_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    """
    Validar si el usuario actual es el propietario o tiene rol de Superadmin.
    """
    # Si el usuario no es Superadmin y no es el propietario del recurso
    if current_user.TipoUsuario != 'Superadmin' and current_user.IdUsuario != user_id:
        raise HTTPException(status_code=403, detail="No tienes permiso para acceder a este recurso")
    
    return current_user  # Retorna el usuario actual para su uso posterior
