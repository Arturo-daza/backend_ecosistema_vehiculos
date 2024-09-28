from sqlalchemy.orm import Session
from models.sparepart import SparePart as SparePartModel
from schemas.sparepart import SparePartCreate, SparePartUpdate

class SparePartService:
    def __init__(self, db: Session):
        self.db = db

    def get_spare_part(self, spare_part_id: int):
        return self.db.query(SparePartModel).filter(SparePartModel.IdRepuesto == spare_part_id).first()

    def get_spare_parts(self, skip: int = 0, limit: int = 100):
        return self.db.query(SparePartModel).offset(skip).limit(limit).all()

    def create_spare_part(self, spare_part: SparePartCreate):
        db_spare_part = SparePartModel(**spare_part.dict())
        self.db.add(db_spare_part)
        self.db.commit()
        self.db.refresh(db_spare_part)
        return db_spare_part

    def update_spare_part(self, spare_part_id: int, spare_part: SparePartUpdate):
        db_spare_part = self.get_spare_part(spare_part_id)
        if not db_spare_part:
            return None
        for key, value in spare_part.dict(exclude_unset=True).items():
            setattr(db_spare_part, key, value)
        self.db.commit()
        self.db.refresh(db_spare_part)
        return db_spare_part

    def delete_spare_part(self, spare_part_id: int):
        db_spare_part = self.get_spare_part(spare_part_id)
        if not db_spare_part:
            return False
        self.db.delete(db_spare_part)
        self.db.commit()
        return True
