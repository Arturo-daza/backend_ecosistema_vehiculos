from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.database import Database
from middlewares.jwt_bearer import JWTBearer
from schemas.service_performed_spare_part import ServicePerformedSparePartCreate, ServicePerformedSparePartResponse
from services.service_performed_spare_part import ServicePerformedSparePartService

service_performed_spare_part_router = APIRouter()

get_db = Database.get_instance().get_db

# Añadir repuesto a un servicio realizado
@service_performed_spare_part_router.post("/{service_performed_id}/spare-parts/", response_model=ServicePerformedSparePartResponse, dependencies=[Depends(JWTBearer())] )
def add_spare_part_to_service(service_performed_id: int, spare_part: ServicePerformedSparePartCreate, db: Session = Depends(get_db)):
    spare_part_service = ServicePerformedSparePartService(db)
    if spare_part.IdServicioRealizado != service_performed_id:
        raise HTTPException(status_code=400, detail="Invalid service ID")
    
    db_spare_part = spare_part_service.add_spare_part_to_service(spare_part)
    return db_spare_part

# Obtener los repuestos de un servicio realizado
@service_performed_spare_part_router.get("/{service_performed_id}/spare-parts/", response_model=list[ServicePerformedSparePartResponse], dependencies=[Depends(JWTBearer())])
def get_spare_parts_by_service(service_performed_id: int, db: Session = Depends(get_db)):
    spare_part_service = ServicePerformedSparePartService(db)
    return spare_part_service.get_spare_parts_by_service(service_performed_id)

# Eliminar un repuesto de un servicio realizado
@service_performed_spare_part_router.delete("/{service_performed_id}/spare-parts/{spare_part_id}", status_code=204, dependencies=[Depends(JWTBearer())])
def delete_spare_part_from_service(service_performed_id: int, spare_part_id: int, db: Session = Depends(get_db)):
    spare_part_service = ServicePerformedSparePartService(db)
    success = spare_part_service.delete_spare_part_from_service(service_performed_id, spare_part_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Spare part not found in this service")
    
    return {"message": "Spare part removed from service"}
