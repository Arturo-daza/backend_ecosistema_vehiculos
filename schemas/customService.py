from pydantic import BaseModel, Field, conint, condecimal
from decimal import Decimal
from typing import Optional


class CustomServiceBase(BaseModel):
    IdServicio: int
    IdUsuario: int
    ValorPropietario: int
    TiempoPropietario: int
    NombreNegocio: str

class CustomServiceCreate(CustomServiceBase):
    pass

class CustomServiceUpdate(BaseModel):
    ValorPropietario: Optional[int] 
    TiempoPropietario: Optional[int]
    NombreNegocio: Optional[str]

class CustomService(CustomServiceBase):
    IdServicioPersonalizado: int

    class Config:
        from_attributes = True
