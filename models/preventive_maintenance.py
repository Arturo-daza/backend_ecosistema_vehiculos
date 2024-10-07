from sqlalchemy import Column, Integer, String, Enum, Date, Text, ForeignKey
from config.database import Base

class PreventiveMaintenance(Base):
    __tablename__ = 'MantenimientoPreventivo'

    IdMantenimientoPreventivo = Column(Integer, primary_key=True, autoincrement=True)
    IdVehiculo = Column(String(20), ForeignKey('Vehiculo.Placa'), nullable=False)
    IdServicio = Column(Integer, ForeignKey('Servicio.IdServicio'), nullable=False)
    KilometrajeRecomendado = Column(Integer, nullable=False)
    FrecuenciaTipo = Column(Enum('Tiempo', 'Kilometraje'), nullable=False)
    FrecuenciaValor = Column(Integer)
    FechaUltimoMantenimiento = Column(Date)
    Notas = Column(Text)
