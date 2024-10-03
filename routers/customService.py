from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.database import Database
from dependencies.get_current_user import get_current_user
from dependencies.validate_user_access import validate_user_access
from middlewares.jwt_bearer import JWTBearer
from schemas.customService import CustomService, CustomServiceCreate, CustomServiceUpdate
from services.customService import CustomServiceService
from schemas.user import User as UserSchema


database = Database.get_instance()
get_db = database.get_db

custom_service_router = APIRouter()

@custom_service_router.post("/custom_services/", response_model=CustomService, dependencies=[Depends(JWTBearer())])
def create_custom_service(custom_service: CustomServiceCreate, db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    custom_service_service = CustomServiceService(db)
    return custom_service_service.create_custom_service(custom_service)

@custom_service_router.get("/custom_services/{custom_service_id}", response_model=CustomService, dependencies=[Depends(JWTBearer())])
def get_custom_service(custom_service_id: int, db: Session = Depends(get_db), current_user: UserSchema = Depends(validate_user_access)):
    custom_service_service = CustomServiceService(db)
    db_custom_service = custom_service_service.get_custom_service(custom_service_id)
    if db_custom_service is None:
        raise HTTPException(status_code=404, detail="Custom service not found")
    return db_custom_service

@custom_service_router.put("/custom_services/{custom_service_id}", response_model=CustomService, dependencies=[Depends(JWTBearer())])
def update_custom_service(custom_service_id: int, custom_service: CustomServiceUpdate, db: Session = Depends(get_db) , current_user: UserSchema = Depends(validate_user_access)):
    custom_service_service = CustomServiceService(db)
    db_custom_service = custom_service_service.update_custom_service(custom_service_id, custom_service)
    if db_custom_service is None:
        raise HTTPException(status_code=404, detail="Custom service not found")
    return db_custom_service

@custom_service_router.delete("/custom_services/{custom_service_id}", dependencies=[Depends(JWTBearer())])
def delete_custom_service(custom_service_id: int, db: Session = Depends(get_db), current_user: UserSchema = Depends(validate_user_access)):
    custom_service_service = CustomServiceService(db)
    if not custom_service_service.delete_custom_service(custom_service_id):
        raise HTTPException(status_code=404, detail="Custom service not found")
    return {"message": "Custom service deleted successfully"}
