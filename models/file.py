from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from config.database import Base 

class File(Base):
    __tablename__ = 'Archivo'

    IdArchivo = Column(Integer, primary_key=True, autoincrement=True)  # ID autoincremental
    NombreArchivo = Column(String(255), nullable=False)  # Nombre del archivo
    Ruta = Column(String(255), nullable=False)  # Ruta o URL donde se almacena el archivo
    TipoArchivo = Column(String(50), nullable=False)  # Tipo o extensión del archivo (ej: jpg, pdf)
    FechaSubida = Column(DateTime, default=datetime.now())  # Fecha de subida del archivo

    def __repr__(self):
        return f"<Archivo(IdArchivo={self.IdArchivo}, NombreArchivo='{self.NombreArchivo}', Ruta='{self.Ruta}', TipoArchivo='{self.TipoArchivo}')>"
