from pydantic import BaseModel
from typing import Optional

class LocationBase(BaseModel):
    Latitud: float
    Longitud: float
    Direccion: Optional[str] = None
    Ciudad: Optional[str]= None
    Pais: Optional[str]= None

class LocationCreate(LocationBase):
    pass

class Location(LocationBase):
    IdUbicacion: int

    class Config:
        from_attributes = True
