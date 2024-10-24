from pydantic import BaseModel
from typing import Optional
from decimal import Decimal
from datetime import datetime, date

class FuelRefillBase(BaseModel):
    IdVehiculo: str
    Kilometraje: int
    GalonesTanqueados: Decimal
    TipoCombustible: str
    PrecioGalon: Decimal
    EstacionServicio: Optional[str]
    IdUbicacion: Optional[int]
    Date: Optional[date]

    class Config:
        from_attributes = True

class FuelRefillCreate(FuelRefillBase):
    pass

class FuelRefillResponse(FuelRefillBase):
    IdRecargaCombustible: int
    Date: Optional[date]
    CostoTotal: Decimal

    class Config:
        from_attributes = True

class FuelRefillUpdate(BaseModel):
    IdVehiculo: Optional[str]
    Kilometraje: Optional[int]
    GalonesTanqueados: Optional[Decimal]
    TipoCombustible: Optional[str]
    PrecioGalon: Optional[Decimal]
    EstacionServicio: Optional[str]
    IdUbicacion: Optional[int]
    Date: Optional[date]

    class Config:
        from_attributes = True