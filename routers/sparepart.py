from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.sparepart import SparePartCreate, SparePartUpdate, SparePartInDB
from services.sparepart import SparePartService
from dependencies import get_current_user
from config.database import Database

sparepart_router = APIRouter()
get_db = Database.get_instance().get_db

@sparepart_router.post("/spare-parts/", response_model=SparePartInDB)
def create_spare_part(spare_part: SparePartCreate, db: Session = Depends(get_db)):
    spare_part_service = SparePartService(db)
    return spare_part_service.create_spare_part(spare_part)

@sparepart_router.get("/spare-parts/{spare_part_id}", response_model=SparePartInDB)
def get_spare_part(spare_part_id: int, db: Session = Depends(get_db)):
    spare_part_service = SparePartService(db)
    db_spare_part = spare_part_service.get_spare_part(spare_part_id)
    if db_spare_part is None:
        raise HTTPException(status_code=404, detail="Spare part not found")
    return db_spare_part

@sparepart_router.put("/spare-parts/{spare_part_id}", response_model=SparePartInDB)
def update_spare_part(spare_part_id: int, spare_part: SparePartUpdate, db: Session = Depends(get_db)):
    spare_part_service = SparePartService(db)
    db_spare_part = spare_part_service.update_spare_part(spare_part_id, spare_part)
    if db_spare_part is None:
        raise HTTPException(status_code=404, detail="Spare part not found")
    return db_spare_part

@sparepart_router.delete("/spare-parts/{spare_part_id}")
def delete_spare_part(spare_part_id: int, db: Session = Depends(get_db)):
    spare_part_service = SparePartService(db)
    success = spare_part_service.delete_spare_part(spare_part_id)
    if not success:
        raise HTTPException(status_code=404, detail="Spare part not found")
    return {"message": "Spare part deleted successfully"}
