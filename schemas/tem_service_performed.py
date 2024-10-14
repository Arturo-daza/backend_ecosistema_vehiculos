from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TempServicePerformedBase(BaseModel):
    PlacaVehiculo: str
    TipoServicio: str
    NombreNegocio: str
    ValorServicio: float
    Duracion: Optional[int] = None
    FotoServicio: Optional[int] = None
    Comentarios: Optional[str] = None

    # Campos adicionales para taller
    Kilometraje: Optional[int] = None
    Concepto: Optional[str] = None
    Repuestos: Optional[str] = None
    DescripcionFalla: Optional[str] = None
    Diagnostico: Optional[str] = None

    class Config:
        from_attributes = True

class TempServicePerformedCreate(TempServicePerformedBase):
    pass

class TempServicePerformed(TempServicePerformedBase):
    IdServicioRealizado: int
    Fecha: Optional[datetime]

    class Config:
        from_attributes = True
