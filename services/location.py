from sqlalchemy.orm import Session
from models.location import Location as LocationModel
from schemas.location import LocationCreate

class LocationService:
    def __init__(self, db: Session):
        self.db = db

    def create_location(self, location: LocationCreate):
        db_location = LocationModel(**location.model_dump())
        self.db.add(db_location)
        self.db.commit()
        self.db.refresh(db_location)
        return db_location

    def get_location(self, location_id: int):
        return self.db.query(LocationModel).filter(LocationModel.IdUbicacion == location_id).first()

    def get_locations(self, skip: int = 0, limit: int = 100):
        return self.db.query(LocationModel).offset(skip).limit(limit).all()

    def update_location(self, location_id: int, location: LocationCreate):
        db_location = self.db.query(LocationModel).filter(LocationModel.IdUbicacion == location_id).first()
        if db_location:
            for var, value in location.dict(exclude_unset=True).items():
                setattr(db_location, var, value)
            self.db.commit()
            self.db.refresh(db_location)
            return db_location
        return None

    def delete_location(self, location_id: int):
        db_location = self.db.query(LocationModel).filter(LocationModel.IdUbicacion == location_id).first()
        if db_location:
            self.db.delete(db_location)
            self.db.commit()
            return True
        return False
