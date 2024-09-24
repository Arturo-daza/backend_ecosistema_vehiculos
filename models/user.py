from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'Usuario'
    IdUsuario = Column(Integer, primary_key=True, autoincrement=True)
    Nombre = Column(String(255), nullable=False)
    NumeroDocumento = Column(String(20), unique=True)
    Email = Column(String(255), unique=True, nullable=False)
    Contrasena = Column(String(255), nullable=False)
    Telefono = Column(String(20))
    FotoPerfil = Column(String(255))
    FechaRegistro = Column(DateTime, default=datetime.now())
    Activo = Column(Boolean, default=True)
    TipoUsuario = Column(Enum('Normal', 'Negocio', 'Superadmin'), nullable=False)
    IdRol = Column(Integer, ForeignKey('Rol.IdRol'), nullable= True)

    rol = relationship("Rol", backref="usuarios")

class Rol(Base):
    __tablename__ = 'Rol'
    IdRol = Column(Integer, primary_key=True, autoincrement=True)
    Nombre = Column(String(50), nullable=False)
    Descripcion = Column(Text)