from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from datetime import datetime

class User(BaseModel):
    IdUsuario: Optional[int] = None
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

    
class UserUpdate(BaseModel):
    Nombre: Optional[str]
    NumeroDocumento: Optional[str]
    Email: Optional[EmailStr]
    Contrasena: Optional[str]
    Telefono: Optional[str]
    FotoPerfil: Optional[str]
    TipoUsuario: Optional[str]
    IdRol: Optional[int]

    @field_validator('TipoUsuario')
    def validate_tipo_usuario(cls, value):
        if value is not None and value not in ['Normal', 'Negocio']:
            raise ValueError("Tipo de usuario inválido. Debe ser 'Normal' o 'Negocio'.")
        return value

class Rol(BaseModel):
    IdRol: int
    Nombre: str
    Descripcion: Optional[str]
    class Config:
        from_attributes = True