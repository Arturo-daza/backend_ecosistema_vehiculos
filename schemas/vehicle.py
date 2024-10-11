from pydantic import BaseModel
from typing import Optional

class Vehicle(BaseModel):
    Placa: str
    IdUsuario: int
    Tipo: str
    Marca: str
    Modelo: str
    Color: Optional[str] = None
    NumeroChasis: Optional[str]= None
    NumeroMotor: Optional[str]= None
    TipoCombustible: Optional[str]= None
    KilometrajeActual: Optional[int]= None
    IdFoto: Optional[int]= None

    class Config:
        from_attributes = True
        
class VehicleUpdate(BaseModel):
    IdUsuario: int
    Tipo: str
    Marca: str
    Modelo: str
    Color: Optional[str] = None
    NumeroChasis: Optional[str]= None
    NumeroMotor: Optional[str]= None
    TipoCombustible: Optional[str]= None
    KilometrajeActual: Optional[int]= None
    IdFoto: Optional[int]= None

    class Config:
        from_attributes = True

class VehicleResponse(Vehicle):
    urlFoto: Optional[str] = None

    class Config:
        from_attributes = True
