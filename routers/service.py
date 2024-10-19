from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.database import Database
from dependencies.get_current_user import get_current_user
from middlewares.jwt_bearer import JWTBearer
from schemas.service import ServicioCreate, ServicioUpdate, ServicioOut
from services.service import ServiceService
from schemas.user import User as UserSchema
from dependencies.validate_user_access import validate_user_access

database = Database.get_instance()
get_db = database.get_db

service_router = APIRouter()

@service_router.post("/", response_model=ServicioOut, dependencies=[Depends(JWTBearer())])
def create_servicio(servicio: ServicioCreate, db: Session = Depends(get_db)):
    servicio_service = ServiceService(db)
    return servicio_service.create_servicio(servicio=servicio)

@service_router.get("/maintenance_service", response_model=list[ServicioOut], dependencies=[Depends(JWTBearer())])
def get_servicios(db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    servicio_service = ServiceService(db)
    return servicio_service.get_services_by_user(5)

@service_router.get("/{servicio_id}", response_model=ServicioOut, dependencies=[Depends(JWTBearer())]
)
def get_servicio(servicio_id: int, db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)
):
    servicio_service = ServiceService(db)
    db_servicio = servicio_service.get_servicio(servicio_id)
    if db_servicio is None:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    return db_servicio

@service_router.get("/", response_model=list[ServicioOut], dependencies=[Depends(JWTBearer())]
)
def get_servicios(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)
):
    servicio_service = ServiceService(db)
    return servicio_service.get_servicios(skip=skip, limit=limit)

@service_router.put("/{servicio_id}", response_model=ServicioOut, dependencies=[Depends(JWTBearer())]
)
def update_servicio(servicio_id: int, servicio: ServicioUpdate, db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)
):
    servicio_service = ServiceService(db)
    updated_servicio = servicio_service.update_servicio(servicio_id, servicio)
    if updated_servicio is None:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    return updated_servicio

@service_router.delete("/{servicio_id}", status_code=204, dependencies=[Depends(JWTBearer())])
def delete_servicio(servicio_id: int, db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)
):
    servicio_service = ServiceService(db)
    success = servicio_service.delete_servicio(servicio_id)
    if not success:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    return {"message": "Servicio eliminado exitosamente"}





