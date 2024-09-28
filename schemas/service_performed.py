from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ServicePerformedBase(BaseModel):
    IdServicio: int
    Fecha: Optional[datetime] = datetime.now()
    Precio: float
    Duracion: Optional[int] = None
    Diagnostico: Optional[str] = None
    Descripcion: Optional[str] = None
    Kilometraje: Optional[int] = None
    IdFotoAntes: Optional[int] = None
    IdFotoDespues: Optional[int] = None
    IdUbicacion: Optional[int] = None
    Estado: Optional[str] = None
    VinculadoANegocio: Optional[bool] = None
    IdUsuarioNegocio: Optional[int] = None
    IdVehiculo: str
    # IdCita: Optional[int] = None
    
class ServicePerformedCreate(ServicePerformedBase):
    pass

class ServicePerformed(ServicePerformedBase):
    IdServicioRealizado: int

    class Config:
        from_attributes = True
