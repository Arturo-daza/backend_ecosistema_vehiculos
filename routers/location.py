from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.database import Database
from dependencies.get_current_user import get_current_user
from dependencies.validate_user_access import validate_user_access
from middlewares.jwt_bearer import JWTBearer
from schemas.location import LocationCreate, Location
from services.location import LocationService
from schemas.user import User as UserSchema



get_db = Database.get_instance().get_db

location_router = APIRouter()

@location_router.post("/locations/", response_model=Location, dependencies=[Depends(JWTBearer())])
def create_location(location: LocationCreate, db: Session = Depends(get_db)):
    location_service = LocationService(db)
    return location_service.create_location(location)

@location_router.get("/locations/{location_id}", response_model=Location, dependencies=[Depends(JWTBearer())])
def get_location(location_id: int, db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)
):
    location_service = LocationService(db)
    db_location = location_service.get_location(location_id)
    if not db_location:
        raise HTTPException(status_code=404, detail="Location not found")
    return db_location

@location_router.get("/locations/", response_model=list[Location], dependencies=[Depends(JWTBearer())])
def get_locations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)
):
    location_service = LocationService(db)
    return location_service.get_locations(skip=skip, limit=limit)

@location_router.put("/locations/{location_id}", response_model=Location, dependencies=[Depends(JWTBearer())])
def update_location(location_id: int, location: LocationCreate, db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)
):
    location_service = LocationService(db)
    db_location = location_service.update_location(location_id, location)
    if not db_location:
        raise HTTPException(status_code=404, detail="Location not found")
    return db_location

@location_router.delete("/locations/{location_id}", response_model=bool)
def delete_location(location_id: int, db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)
):
    location_service = LocationService(db)
    return location_service.delete_location(location_id)
