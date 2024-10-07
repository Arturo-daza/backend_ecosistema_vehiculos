from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.database import Database
from dependencies.get_current_user import get_current_user
from dependencies.validate_user_access import validate_user_access
from middlewares.jwt_bearer import JWTBearer
from schemas.preventive_maintenance import PreventiveMaintenanceCreate, PreventiveMaintenanceUpdate, PreventiveMaintenance
from services.preventive_maintenance import PreventiveMaintenanceService
from schemas.user import User as UserSchema

preventive_maintenance_router = APIRouter()

get_db = Database.get_instance().get_db

@preventive_maintenance_router.post("/", response_model=PreventiveMaintenance, dependencies=[Depends(JWTBearer())])
def create_maintenance(maintenance: PreventiveMaintenanceCreate, db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    maintenance_service = PreventiveMaintenanceService(db)
    return maintenance_service.create_maintenance(maintenance)

@preventive_maintenance_router.get("/{maintenance_id}", response_model=PreventiveMaintenance, dependencies=[Depends(JWTBearer())])
def get_maintenance(maintenance_id: int, db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    maintenance_service = PreventiveMaintenanceService(db)
    db_maintenance = maintenance_service.get_maintenance(maintenance_id)
    if not db_maintenance:
        raise HTTPException(status_code=404, detail="Maintenance not found")
    return db_maintenance

@preventive_maintenance_router.get("/vehicles/{vehicle_id}", response_model=list[PreventiveMaintenance], dependencies=[Depends(JWTBearer())])
def get_maintenances_by_vehicle(vehicle_id: str, db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    maintenance_service = PreventiveMaintenanceService(db)
    return maintenance_service.get_maintenances_by_vehicle(vehicle_id)

@preventive_maintenance_router.put("/{maintenance_id}", response_model=PreventiveMaintenance)
def update_maintenance(maintenance_id: int, maintenance: PreventiveMaintenanceUpdate, db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    maintenance_service = PreventiveMaintenanceService(db)
    updated_maintenance = maintenance_service.update_maintenance(maintenance_id, maintenance)
    if not updated_maintenance:
        raise HTTPException(status_code=404, detail="Maintenance not found")
    return updated_maintenance

@preventive_maintenance_router.delete("/{maintenance_id}", status_code=204,  dependencies=[Depends(JWTBearer())])
def delete_maintenance(maintenance_id: int, db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    maintenance_service = PreventiveMaintenanceService(db)
    if not maintenance_service.delete_maintenance(maintenance_id):
        raise HTTPException(status_code=404, detail="Maintenance not found")
    return {"message": "Maintenance deleted successfully"}
