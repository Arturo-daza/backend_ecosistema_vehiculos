from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import date

class PreventiveMaintenanceBase(BaseModel):
    IdVehiculo: str
    IdServicio: int
    KilometrajeRecomendado: Optional[int]
    FrecuenciaTipo: str = 'Kilometraje'
    FrecuenciaValor:int 
    FechaUltimoMantenimiento: Optional[date]
    Notas: Optional[str]
    @field_validator('FrecuenciaTipo')
    def validate_tipo_usuario(cls, value):
        if value not in ['Kilometraje', 'Tiempo']:
            raise ValueError("Frecuencia tipo invalidad. Debe ser 'Tiempo' o 'Kilometraje'.")
        return value
    

    class Config:
        from_attributes = True

class PreventiveMaintenanceCreate(PreventiveMaintenanceBase):
    pass

class PreventiveMaintenanceUpdate(PreventiveMaintenanceBase):
    pass

class PreventiveMaintenance(PreventiveMaintenanceBase):
    IdMantenimientoPreventivo: int

    class Config:
        from_attributes = True
