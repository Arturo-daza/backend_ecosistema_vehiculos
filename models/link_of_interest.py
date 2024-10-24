from sqlalchemy import Column, Integer, String, Text
from config.database import Base

class LinkOfInterest(Base):
    __tablename__ = 'EnlacesInteres'

    IdEnlace = Column(Integer, primary_key=True, autoincrement=True)
    Nombre = Column(String(255), nullable=False)
    Descripcion = Column(Text, nullable=True)
    URL = Column(String(500), nullable=False)
