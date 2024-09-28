from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, DECIMAL, Text, Enum, Boolean
from sqlalchemy.orm import relationship
from config.database import Base
from datetime import datetime

class ServicePerformed(Base):
    __tablename__ = 'ServicioRealizado'

    IdServicioRealizado = Column(Integer, primary_key=True, index=True)
    IdServicio = Column(Integer, ForeignKey('Servicio.IdServicio'), nullable=False)
    Fecha = Column(DateTime, default=datetime.now)
    Precio = Column(DECIMAL(10, 2), nullable=False)
    Duracion = Column(Integer)
    Diagnostico = Column(Text)
    Descripcion = Column(Text)
    Kilometraje = Column(Integer)
    IdFotoAntes = Column(Integer, ForeignKey('Archivo.IdArchivo'))
    IdFotoDespues = Column(Integer, ForeignKey('Archivo.IdArchivo'))
    IdUbicacion = Column(Integer, ForeignKey('Ubicacion.IdUbicacion'))
    Estado = Column(Enum('Pendiente', 'En Proceso', 'Completado', 'Cancelado'), default='Pendiente')
    VinculadoANegocio = Column(Boolean, default=False)
    IdUsuarioNegocio = Column(Integer, ForeignKey('Usuario.IdUsuario'))
    IdVehiculo = Column(String(20), ForeignKey('Vehiculo.Placa'), nullable=False)
    # IdCita = Column(Integer, ForeignKey('Cita.IdCita'))

    # Relaciones
    repuestos = relationship("ServicioRealizadoRepuesto", back_populates="servicio_realizado")
