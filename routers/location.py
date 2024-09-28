from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.database import Database
from schemas.location import LocationCreate, Location
from services.location import LocationService

get_db = Database.get_instance().get_db

location_router = APIRouter()

@location_router.post("/locations/", response_model=Location)
def create_location(location: LocationCreate, db: Session = Depends(get_db)):
    location_service = LocationService(db)
    return location_service.create_location(location)

@location_router.get("/locations/{location_id}", response_model=Location)
def get_location(location_id: int, db: Session = Depends(get_db)):
    location_service = LocationService(db)
    db_location = location_service.get_location(location_id)
    if not db_location:
        raise HTTPException(status_code=404, detail="Location not found")
    return db_location

@location_router.get("/locations/", response_model=list[Location])
def get_locations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    location_service = LocationService(db)
    return location_service.get_locations(skip=skip, limit=limit)

@location_router.put("/locations/{location_id}", response_model=Location)
def update_location(location_id: int, location: LocationCreate, db: Session = Depends(get_db)):
    location_service = LocationService(db)
    db_location = location_service.update_location(location_id, location)
    if not db_location:
        raise HTTPException(status_code=404, detail="Location not found")
    return db_location

@location_router.delete("/locations/{location_id}", response_model=bool)
def delete_location(location_id: int, db: Session = Depends(get_db)):
    location_service = LocationService(db)
    return location_service.delete_location(location_id)
