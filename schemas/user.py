from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    Nombre: str
    NumeroDocumento: Optional[str]
    Email: EmailStr
    Contrasena: str
    Telefono: Optional[str]
    FotoPerfil: Optional[str]
    TipoUsuario: str = 'Normal'
    FechaRegistro: Optional[datetime] = None
    Activo: Optional[bool] = True
    IdRol: Optional[int] = None

    @field_validator('TipoUsuario')
    def validate_tipo_usuario(cls, value):
        if value not in ['Normal', 'Negocio', 'Superadmin']:
            raise ValueError("Tipo de usuario inválido. Debe ser 'Normal' o 'Negocio'.")
        return value

class User(UserBase):
    IdUsuario: Optional[int] = None

    
class UserUpdate(UserBase):
    pass

class UserCreate(UserBase):
    pass

class Rol(BaseModel):
    IdRol: int
    Nombre: str
    Descripcion: Optional[str]
    class Config:
        from_attributes = True