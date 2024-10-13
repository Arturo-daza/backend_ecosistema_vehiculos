from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.database import Database
from schemas.fuel_refill import FuelRefillCreate, FuelRefillResponse
from services.fuel_refill import FuelRefillService

fuel_refill_router = APIRouter()

get_db = Database.get_instance().get_db

# Crear recarga de combustible
@fuel_refill_router.post("/", response_model=FuelRefillResponse)
def create_fuel_refill(refill: FuelRefillCreate, db: Session = Depends(get_db)):
    refill_service = FuelRefillService(db)
    return refill_service.create_fuel_refill(refill)

# Obtener una recarga de combustible por ID
@fuel_refill_router.get("/{refill_id}", response_model=FuelRefillResponse)
def get_fuel_refill(refill_id: int, db: Session = Depends(get_db)):
    refill_service = FuelRefillService(db)
    db_refill = refill_service.get_fuel_refill(refill_id)
    if not db_refill:
        raise HTTPException(status_code=404, detail="Recarga de combustible no encontrada")
    return db_refill

# Obtener todas las recargas de combustible de un vehículo
@fuel_refill_router.get("/vehicles/{vehicle_id}", response_model=list[FuelRefillResponse])
def get_fuel_refills_by_vehicle(vehicle_id: str, db: Session = Depends(get_db)):
    refill_service = FuelRefillService(db)
    return refill_service.get_fuel_refills_by_vehicle(vehicle_id)

# Eliminar una recarga de combustible por ID
@fuel_refill_router.delete("/{refill_id}")
def delete_fuel_refill(refill_id: int, db: Session = Depends(get_db)):
    refill_service = FuelRefillService(db)
    success = refill_service.delete_fuel_refill(refill_id)
    if not success:
        raise HTTPException(status_code=404, detail="Recarga de combustible no encontrada")
    return {"message": "Recarga de combustible eliminada exitosamente"}

# Obtener todas las recargas de combustible de un usuario
@fuel_refill_router.get("/users/{user_id}", response_model=list[FuelRefillResponse])
def get_fuel_refills_by_user(user_id: int, db: Session = Depends(get_db)):
    refill_service = FuelRefillService(db)
    refills = refill_service.get_fuel_refills_by_user(user_id)
    
    if not refills:
        raise HTTPException(status_code=404, detail="No se encontraron recargas de combustible para este usuario")
    
    return refills