from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from config.database import Base
from datetime import datetime

class File(Base):
    __tablename__ = 'Archivo'

    IdArchivo = Column(Integer, primary_key=True, autoincrement=True)
    NombreArchivo = Column(String(255), nullable=False)
    TipoArchivo = Column(String(50))
    Extension = Column(String(10))
    Tamaño = Column(Integer)
    Ruta = Column(String(255), nullable=False)
    FechaSubida = Column(DateTime, default=datetime.now())
    IdUsuarioSubida = Column(Integer, ForeignKey('Usuario.IdUsuario'), nullable=True)
    TipoEntidad = Column(String(50))


    def __repr__(self):
        return f"<Archivo(IdArchivo={self.IdArchivo}, NombreArchivo='{self.NombreArchivo}', Ruta='{self.Ruta}', TipoArchivo='{self.TipoArchivo}')>"
