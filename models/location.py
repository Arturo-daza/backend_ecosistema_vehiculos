from sqlalchemy import Column, Integer, String, DECIMAL
from config.database import Base

class Location(Base):
    __tablename__ = 'Ubicacion'

    IdUbicacion = Column(Integer, primary_key=True, autoincrement=True)
    Latitud = Column(DECIMAL(10, 8), nullable=False)
    Longitud = Column(DECIMAL(11, 8), nullable=False)
    Direccion = Column(String(255))
    Ciudad = Column(String(100))
    Pais = Column(String(100))
