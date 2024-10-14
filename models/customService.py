from sqlalchemy import Column, Integer, ForeignKey, DECIMAL, String
from sqlalchemy.orm import relationship
from models.user import User
from models.service import Service
from config.database import Base

class CustomService(Base):
    __tablename__ = 'ServicioPersonalizado'

    IdServicioPersonalizado = Column(Integer, primary_key=True, autoincrement=True)
    IdServicio = Column(Integer, ForeignKey('Servicio.IdServicio'), nullable=False)
    IdUsuario = Column(Integer, ForeignKey('Usuario.IdUsuario'), nullable=False)
    ValorPropietario = Column(DECIMAL(10, 2), nullable=True)
    TiempoPropietario = Column(Integer, nullable=True)
    NombreNegocio = Column(String(255), nullable=True)

    service = relationship("Service", backref="custom_services")
    user = relationship("User", backref="custom_services")
