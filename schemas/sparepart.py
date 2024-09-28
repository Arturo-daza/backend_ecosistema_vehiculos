from pydantic import BaseModel
from typing import Optional

class SparePartBase(BaseModel):
    Nombre: str
    Descripcion: Optional[str] = None
    Marca: Optional[str] = None
    Modelo: Optional[str] = None
    Compatibilidad: Optional[str] = None  
    IdFoto: Optional[int] = None

class SparePartCreate(SparePartBase):
    pass

class SparePartUpdate(SparePartBase):
    pass

class SparePartInDB(SparePartBase):
    IdRepuesto: int

    class Config:
        from_attributes = True