from pydantic import BaseModel, Field
from typing import Optional

class ServicioBase(BaseModel):
    Nombre: str
    Descripcion: Optional[str] = None
    CreadoPorUsuario: Optional[bool] = True
    IdImagenServicio: Optional[int] = None

class ServicioCreate(ServicioBase):
    pass

class ServicioUpdate(ServicioBase):
    pass

class ServicioOut(ServicioBase):
    IdServicio: int

    class Config:
        from_attributes = True
