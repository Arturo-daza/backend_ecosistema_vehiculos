from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import date

class PreventiveMaintenanceBase(BaseModel):
    IdVehiculo: str
    IdServicio: int
    FrecuenciaTipo: str = 'Kilometraje'  # Puede ser 'Kilometraje' o 'Tiempo'
    FrecuenciaKilometraje: Optional[int]  # Frecuencia basada en kilometraje
    FrecuenciaTiempo: Optional[int]  # Frecuencia basada en tiempo
    FrecuenciaTiempoTipo: Optional[str] = 'Meses'  # Puede ser 'Dias', 'Semanas', 'Meses', 'Años'
    FechaUltimoMantenimiento: Optional[date]  # Fecha del último mantenimiento
    KilometrajeUltimoMantenimiento: Optional[int]  # Kilometraje al momento del último mantenimiento
    Notas: Optional[str]

    @field_validator('FrecuenciaTipo')
    def validate_frecuencia_tipo(cls, value):
        if value not in ['Kilometraje', 'Tiempo']:
            raise ValueError("Frecuencia tipo inválida. Debe ser 'Tiempo' o 'Kilometraje'.")
        return value

    @field_validator('FrecuenciaTiempoTipo')
    def validate_frecuencia_tiempo_tipo(cls, value):
        if value not in ['Dias', 'Semanas', 'Meses', 'Años']:
            raise ValueError("Frecuencia tiempo tipo inválida. Debe ser 'Dias', 'Semanas', 'Meses', o 'Años'.")
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
