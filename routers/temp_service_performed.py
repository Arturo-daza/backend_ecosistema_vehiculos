from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.database import Database
from middlewares.jwt_bearer import JWTBearer
from schemas.tem_service_performed import TempServicePerformedCreate, TempServicePerformed, TempServicePerformedUpdate
from services.tem_service_performed import TempServicePerformedService

temp_service_performed_router = APIRouter()

get_db = Database.get_instance().get_db

# Crear servicio realizado
@temp_service_performed_router.post("/services_performed/", response_model=TempServicePerformed,dependencies=[Depends(JWTBearer())])
def create_service_performed(service_performed: TempServicePerformedCreate, db: Session = Depends(get_db)):
    service_performed_service = TempServicePerformedService(db)
    return service_performed_service.create_service_performed(service_performed)

# Obtener un servicio realizado por ID
@temp_service_performed_router.get("/services_performed/{service_performed_id}", response_model=TempServicePerformed,dependencies=[Depends(JWTBearer())])
def get_service_performed(service_performed_id: int, db: Session = Depends(get_db)):
    service_performed_service = TempServicePerformedService(db)
    db_service_performed = service_performed_service.get_service_performed(service_performed_id)
    if not db_service_performed:
        raise HTTPException(status_code=404, detail="Servicio realizado no encontrado")
    return db_service_performed

# Obtener servicios realizados por vehículo
@temp_service_performed_router.get("/vehicles/{placa_vehiculo}/services_performed", response_model=list[TempServicePerformed],dependencies=[Depends(JWTBearer())])
def get_services_by_vehicle(placa_vehiculo: str, db: Session = Depends(get_db)):
    service_performed_service = TempServicePerformedService(db)
    return service_performed_service.get_services_by_vehicle(placa_vehiculo)

# Eliminar un servicio realizado
@temp_service_performed_router.delete("/services_performed/{service_performed_id}",dependencies=[Depends(JWTBearer())])
def delete_service_performed(service_performed_id: int, db: Session = Depends(get_db)):
    service_performed_service = TempServicePerformedService(db)
    success = service_performed_service.delete_service_performed(service_performed_id)
    if not success:
        raise HTTPException(status_code=404, detail="Servicio realizado no encontrado")
    return {"message": "Servicio realizado eliminado exitosamente"}

# Obtener todos los servicios realizados por un usuario
@temp_service_performed_router.get("/users/{user_id}/services_performed", response_model=list[TempServicePerformed],dependencies=[Depends(JWTBearer())])
def get_services_by_user(user_id: int, db: Session = Depends(get_db)):
    service_performed_service = TempServicePerformedService(db)
    services = service_performed_service.get_services_by_user(user_id)
    if not services:
        raise HTTPException(status_code=404, detail="No se encontraron servicios realizados para este usuario")
    return services

# Obtener negocios, conceptos y repuestos vinculados a los servicios realizados por el usuario
@temp_service_performed_router.get("/users/{user_id}/service-data", response_model=dict,dependencies=[Depends(JWTBearer())])
def get_service_data(user_id: int, db: Session = Depends(get_db)):
    service_performed_service = TempServicePerformedService(db)
    data = service_performed_service.get_business_concepts_spareparts(user_id)
    
    if not data:
        raise HTTPException(status_code=404, detail="No se encontraron servicios realizados para este usuario")

    return data

@temp_service_performed_router.put("/services_performed/{service_performed_id}", response_model=TempServicePerformed,dependencies=[Depends(JWTBearer())])
def update_service_performed(service_performed_id: int, service_performed: TempServicePerformedUpdate, db: Session = Depends(get_db)):
    service_performed_service = TempServicePerformedService(db)
    updated_service = service_performed_service.update_service_performed(service_performed_id, service_performed)
    
    if not updated_service:
        raise HTTPException(status_code=404, detail="Servicio realizado no encontrado")
    
    return updated_service