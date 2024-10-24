from pydantic import BaseModel, HttpUrl
from typing import Optional

class LinkOfInterestBase(BaseModel):
    Nombre: str
    Descripcion: Optional[str] = None
    URL: HttpUrl

    class Config:
        from_attributes = True

class LinkOfInterestCreate(LinkOfInterestBase):
    pass

class LinkOfInterestUpdate(LinkOfInterestBase):
    pass

class LinkOfInterest(LinkOfInterestBase):
    IdEnlace: int

    class Config:
        from_attributes = True
