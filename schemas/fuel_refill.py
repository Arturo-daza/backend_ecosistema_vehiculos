from pydantic import BaseModel
from typing import Optional
from decimal import Decimal
from datetime import datetime

class FuelRefillBase(BaseModel):
    IdVehiculo: str
    Fecha: datetime = datetime.now()
    Kilometraje: int
    GalonesTanqueados: Decimal
    TipoCombustible: str
    PrecioGalon: Decimal
    EstacionServicio: Optional[str]
    IdUbicacion: Optional[int]

    class Config:
        from_attributes = True

class FuelRefillCreate(FuelRefillBase):
    pass

class FuelRefillResponse(FuelRefillBase):
    IdRecargaCombustible: int
    Fecha: Optional[datetime]
    CostoTotal: Decimal

    class Config:
        from_attributes = True
