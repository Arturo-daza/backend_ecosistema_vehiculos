from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from config.database import Base 

class Vehicle(Base):
    __tablename__ = 'Vehiculo'
    
    Placa = Column(String(20), primary_key=True)
    IdUsuario = Column(Integer, ForeignKey('Usuario.IdUsuario'), nullable=False)
    Tipo = Column(String(50), nullable=False)
    Marca = Column(String(50), nullable=False)
    Modelo = Column(String(50), nullable=False)
    Color = Column(String(20))
    NumeroChasis = Column(String(50), unique=True)
    NumeroMotor = Column(String(50), unique=True)
    TipoCombustible = Column(String(20))
    KilometrajeActual = Column(Integer)
    IdFoto = Column(Integer, ForeignKey('Archivo.IdArchivo'))  # ForeignKey to Archivo

    # Relación con usuario (Usar cadena para evitar ciclos de importación)
    usuario = relationship("User", backref="vehiculos")
    
    # Relación con archivo (foto del vehículo)
    foto = relationship("File", backref="vehiculos")  # Cambiado a "Archivo"
