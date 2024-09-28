from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from middlewares.jwt_bearer import JWTBearer
from schemas.vehicle import Vehicle as VehicleSchema, VehicleUpdate
from schemas.user import User as UserSchema
from services.vehicle import VehicleService
from config.database import Database
from dependencies.get_current_user import get_current_user
from typing import List




vehicle_router = APIRouter()

database = Database.get_instance()
get_db = database.get_db

@vehicle_router.post("/", response_model=VehicleSchema, dependencies=[Depends(JWTBearer())])
def create_vehicle(vehiculo: VehicleSchema, db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    vehiculo_service = VehicleService(db)
    
    # Check if vehicle already exists by plate
    existing_vehicle = vehiculo_service.get_vehiculo_by_placa(vehiculo.Placa)
    if existing_vehicle:
        raise HTTPException(status_code=400, detail="El vehículo ya está registrado")
    
    vehiculo.IdUsuario = current_user.IdUsuario
    
    new_vehicle = vehiculo_service.create_vehiculo(vehiculo)
    
    return new_vehicle


@vehicle_router.put("/{vehicle_id}", response_model=VehicleSchema, dependencies=[Depends(JWTBearer())])
def update_vehicle(vehicle_id: str, vehicle: VehicleUpdate, db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    vehicle_service = VehicleService(db)
    
    # Obtener el vehículo a editar
    existing_vehicle = vehicle_service.get_vehiculo_by_placa(vehicle_id)
    
    # Verificar si el vehículo existe
    if existing_vehicle is None:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")
    
    print(existing_vehicle)
    
    # Verificar si el usuario tiene permiso para editar
    if existing_vehicle.IdUsuario != current_user.IdUsuario and current_user.TipoUsuario != 'Superadmin':
        raise HTTPException(status_code=403, detail="No tienes permiso para editar este vehículo")
    
    # Actualizar los datos del vehículo
    for var, value in vehicle.dict(exclude_unset=True).items():
        setattr(existing_vehicle, var, value)
    
    db.commit()
    db.refresh(existing_vehicle)
    return existing_vehicle

@vehicle_router.get("/vehicles/{user_id}", response_model=List[VehicleSchema],  dependencies=[Depends(JWTBearer())])  
def get_user_vehicles(user_id: int, db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    # Verificar si el usuario actual es el propietario o un super admin
    if current_user.TipoUsuario != 'Superadmin' and current_user.IdUsuario != user_id: 
        raise HTTPException(status_code=403, detail="No tienes permiso para acceder a estos vehículos")

    # Obtener vehículos del usuario
    vehicle_service = VehicleService(db)
    vehicles = vehicle_service.get_vehicles_by_user(user_id)  # Asegúrate de que tengas este método en tu servicio de vehículos

    if vehicles is None or len(vehicles) == 0:
        raise HTTPException(status_code=404, detail="No se encontraron vehículos para este usuario")

    return vehicles

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

@vehicle_router.delete("/vehicles/{vehicle_id}", status_code=204)
def delete_vehicle(vehicle_id: str, db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    # Obtener el vehículo
    vehicle_service = VehicleService(db)
    vehicle = vehicle_service.get_vehiculo_by_placa(vehicle_id)  # Asegúrate de tener este método en tu servicio

    # Verificar si el vehículo existe
    if vehicle is None:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")

    # Verificar si el usuario actual es el propietario o un super admin
    if current_user.IdRol != 1 and vehicle.IdUsuario != current_user.IdUsuario:  # Suponiendo que el rol de super admin tiene IdRol 1
        raise HTTPException(status_code=403, detail="No tienes permiso para eliminar este vehículo")

    # Eliminar el vehículo
    vehicle_service.delete_vehicle(vehicle_id)  # Asegúrate de tener este método en tu servicio
    return None