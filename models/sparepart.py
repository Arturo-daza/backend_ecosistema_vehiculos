from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from config.database import Base

class SparePart(Base):
    __tablename__ = "Repuesto"

    IdRepuesto = Column(Integer, primary_key=True, autoincrement=True)
    Nombre = Column(String(255), nullable=False)
    Descripcion = Column(Text)
    Marca = Column(String(100))
    Modelo = Column(String(100))
    Compatibilidad = Column(Text)
    IdFoto = Column(Integer, ForeignKey("Archivo.IdArchivo"))

    # Relationship
    foto = relationship("File", foreign_keys=[IdFoto])
