from pydantic import BaseModel
from typing import Optional
from datetime import date

class DocumentBase(BaseModel):
    IdVehiculo: str
    TipoDocumento: str
    NombreDocumento: Optional[str]
    FechaEmision: date
    FechaVencimiento: Optional[date]
    TieneFechaVencimiento: Optional[bool] = False
    CostoDocumento: Optional[float] = 0.00
    IdArchivo: int

    class Config:
        from_attributes = True

class DocumentCreate(DocumentBase):
    pass

class DocumentUpdate(DocumentBase):
    pass

class Document(DocumentBase):
    IdDocumento: int
    EstaVencido: Optional[bool] = False
    DiasParaVencer: Optional[int] = 0

    class Config:
        from_attributes = True
