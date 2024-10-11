from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from dependencies.validate_user_access import validate_user_access
from middlewares.jwt_bearer import JWTBearer
from schemas.vehicle import Vehicle as VehicleSchema, VehicleUpdate
from schemas.vehicle import VehicleResponse as VehicleResponseSchema
from schemas.user import User as UserSchema
from services.vehicle import VehicleService
from services.file import FileService
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
@vehicle_router.get("/{user_id}/vehicles", response_model=List[VehicleResponseSchema], dependencies=[Depends(JWTBearer())])
def get_user_vehicles(user_id: int, db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    vehicle_service = VehicleService(db)
    
    # Obtener vehículos del usuario
    vehicles = vehicle_service.get_vehicles_by_user(user_id)
    
    if vehicles is None or len(vehicles) == 0:
        raise HTTPException(status_code=404, detail="No se encontraron vehículos para este usuario")
    
    file_service = FileService(db)
    
    # Crear una lista para almacenar los vehículos con el campo 'urlFoto' agregado
    vehicles_data = []
    
    # Procesar cada vehículo
    for vehicle in vehicles:
        # Crear un diccionario de datos del vehículo
        vehicle_data = vehicle.__dict__.copy()
        
        # Si tiene una foto, agregar la URL al JSON
        if vehicle.IdFoto is not None:
            file = file_service.get_file(vehicle.IdFoto)
            if file is not None:
                vehicle_data["urlFoto"] = file.Ruta  # Añadir la URL de la foto al JSON
            else:
                vehicle_data["urlFoto"] = None
        else:
            vehicle_data["urlFoto"] = None  # Si no tiene foto, devolver null o equivalente
        
        # Añadir el vehículo procesado a la lista
        vehicles_data.append(vehicle_data)
    
    return vehicles_data




@vehicle_router.delete("/{vehicle_id}", status_code=204, dependencies=[Depends(JWTBearer())])
def delete_vehicle(vehicle_id: str, db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    # Obtener el vehículo
    vehicle_service = VehicleService(db)
    vehicle = vehicle_service.get_vehiculo_by_placa(vehicle_id)  
    # Verificar si el vehículo existe
    if vehicle is None:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")


    # Eliminar el vehículo
    vehicle_service.delete_vehicle(vehicle_id)  # Asegúrate de tener este método en tu servicio
    return None

@vehicle_router.get("/{vehicle_id}", response_model=VehicleResponseSchema, dependencies=[Depends(JWTBearer())])
def get_vehicle_by_id(vehicle_id: str, db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    vehicle_service = VehicleService(db)
    
    # Obtener el vehículo por su ID
    vehicle = vehicle_service.get_vehiculo_by_placa(vehicle_id)
    
    # Verificar si el vehículo existe
    if vehicle is None:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")
    
    # Crear un JSON con la información del vehículo
    vehicle_data = vehicle.__dict__.copy()
    
    # Si tiene una foto, agregar la URL al JSON
    if vehicle.IdFoto is not None:
        file_service = FileService(db)
        file = file_service.get_file(vehicle.IdFoto)
        if file is not None:
            vehicle_data["urlFoto"] = file.Ruta  # Añadir la URL de la foto al JSON
        else:
            vehicle_data["urlFoto"] = None
    else:
        vehicle_data["urlFoto"] = None  # Si no tiene foto, devolver null o algo equivalente
    
    return vehicle_data

