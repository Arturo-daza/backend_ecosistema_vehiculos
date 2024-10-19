from config.database import Base
from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, DECIMAL, Text, Enum
from sqlalchemy.orm import relationship


class TempServicePerformed(Base):
    __tablename__ = 'TempServicioRealizado'

    IdServicioRealizado = Column(Integer, primary_key=True, autoincrement=True)
    PlacaVehiculo = Column(String(20), ForeignKey('Vehiculo.Placa'), nullable=False)  # Relación con Vehículo
    TipoServicio = Column(Enum('Parqueadero', 'Taller', 'Lavadero'), nullable=False)  # Enum con los 3 tipos principales
    NombreNegocio = Column(String(255), nullable=False)
    ValorServicio = Column(DECIMAL(10, 2), nullable=False)
    Duracion = Column(Integer, nullable=True)  # En minutos u horas
    FotoServicio = Column(Integer, ForeignKey('Archivo.IdArchivo'), nullable=True)  # Foto asociada
    Comentarios = Column(Text, nullable=True)

    # Solo para servicios de taller
    Kilometraje = Column(Integer, nullable=True)  # Solo para Taller
    Concepto = Column(String(255), nullable=True)  # Tipo de arreglo, solo para Taller
    Repuestos = Column(Text, nullable=True)  # Listado de repuestos usados, solo para Taller
    DescripcionFalla = Column(Text, nullable=True)  # Descripción del problema, solo para Taller
    Diagnostico = Column(Text, nullable=True)  # Diagnóstico de la falla, solo para Taller

    Fecha = Column(DateTime, default=datetime.now)
    
    # Relaciones
    vehiculo = relationship("Vehicle", back_populates="serviciosRealizados")
