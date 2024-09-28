from sqlalchemy import Table, Column, ForeignKey, Integer
from sqlalchemy.orm import relationship
from config.database import Base

# Tabla intermedia entre ServicioRealizado y Repuesto
class ServicioRealizadoRepuesto(Base):
    __tablename__ = 'ServicioRealizado_Repuesto'
    
    IdServicioRealizado = Column(Integer, ForeignKey('ServicioRealizado.IdServicioRealizado'), primary_key=True)
    IdRepuesto = Column(Integer, ForeignKey('Repuesto.IdRepuesto'), primary_key=True)
    Cantidad = Column(Integer, default=1)

    # Relaciones
    servicio_realizado = relationship("ServicePerformed", back_populates="repuestos")
    repuesto = relationship("SparePart", back_populates="servicios_realizados")
