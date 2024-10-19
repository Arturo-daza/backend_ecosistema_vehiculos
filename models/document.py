from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean, DECIMAL
from sqlalchemy.orm import relationship
from config.database import Base

class Document(Base):
    __tablename__ = 'Documento'

    IdDocumento = Column(Integer, primary_key=True, autoincrement=True)
    IdVehiculo = Column(String(20), ForeignKey('Vehiculo.Placa', ondelete="CASCADE"), nullable=False)
    TipoDocumento = Column(String(100), nullable=False)
    NombreDocumento = Column(String(50))
    FechaEmision = Column(Date, nullable=False)
    FechaVencimiento = Column(Date, nullable=True)
    TieneFechaVencimiento = Column(Boolean, default=False)
    CostoDocumento = Column(DECIMAL(10, 2), default=0.00)
    IdArchivo = Column(Integer, ForeignKey('Archivo.IdArchivo'), nullable=False )

    # Relación con Vehiculo
    vehiculo = relationship("Vehicle", back_populates="documentos")
