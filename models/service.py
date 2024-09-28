from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from config.database import Base

class Service(Base):
    __tablename__ = 'Servicio'
    IdServicio = Column(Integer, primary_key=True, autoincrement=True)
    Nombre = Column(String(255), nullable=False)
    Descripcion = Column(Text, nullable=True)
    CreadoPorUsuario = Column(Boolean, default=True)
    IdImagenServicio = Column(Integer, ForeignKey('Archivo.IdArchivo'), nullable=True)

    imagen = relationship("File", backref="servicios")
