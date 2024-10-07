from pydantic import BaseModel
from typing import Optional

class ServicePerformedSparePartBase(BaseModel):
    IdServicioRealizado: int
    IdRepuesto: int
    Cantidad: Optional[int] = 1

    class Config:
        from_attributes = True

class ServicePerformedSparePartCreate(ServicePerformedSparePartBase):
    pass

class ServicePerformedSparePartResponse(ServicePerformedSparePartBase):
    pass
