from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class FileBase(BaseModel):
    NombreArchivo: str
    TipoArchivo: Optional[str]
    Extension: Optional[str]
    Tamaño: Optional[int]
    Ruta: str
    IdUsuarioSubida: Optional[int]
    TipoEntidad: Optional[str]

    class Config:
        from_attributes = True

class FileCreate(FileBase):
    pass

class FileResponse(FileBase):
    IdArchivo: int
    FechaSubida: datetime

    class Config:
        from_attributes = True
