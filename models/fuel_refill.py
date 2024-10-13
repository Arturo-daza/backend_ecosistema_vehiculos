from sqlalchemy import Column, Integer, String, DECIMAL, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from config.database import Base

class FuelRefill(Base):
    __tablename__ = 'RecargaCombustible'

    IdRecargaCombustible = Column(Integer, primary_key=True, autoincrement=True)
    IdVehiculo = Column(String(20), ForeignKey('Vehiculo.Placa'), nullable=False)
    Fecha = Column(DateTime, default=datetime.now())
    Kilometraje = Column(Integer, nullable=False)
    GalonesTanqueados = Column(DECIMAL(10, 2), nullable=False)
    TipoCombustible = Column(String(20), nullable=False)
    PrecioGalon = Column(DECIMAL(10, 2), nullable=False)
    CostoTotal = Column(DECIMAL(10, 2), nullable=False)
    EstacionServicio = Column(String(255), nullable=True)
    IdUbicacion = Column(Integer, ForeignKey('Ubicacion.IdUbicacion'), nullable=True)

    # Relaciones
    vehiculo = relationship("Vehicle", back_populates="recargas")
    ubicacion = relationship("Location")

