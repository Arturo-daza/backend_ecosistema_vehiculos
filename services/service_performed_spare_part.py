from sqlalchemy.orm import Session
from models.service_performed_spare_part import ServicePerformedSparePart as ServicePerformedSparePartModel
from schemas.service_performed_spare_part import ServicePerformedSparePartCreate

class ServicePerformedSparePartService:
    def __init__(self, db: Session):
        self.db = db

    def add_spare_part_to_service(self, spare_part: ServicePerformedSparePartCreate):
        db_spare_part = ServicePerformedSparePartModel(**spare_part.dict())
        self.db.add(db_spare_part)
        self.db.commit()
        return db_spare_part

    def get_spare_parts_by_service(self, service_performed_id: int):
        return self.db.query(ServicePerformedSparePartModel).filter(ServicePerformedSparePartModel.IdServicioRealizado == service_performed_id).all()

    def delete_spare_part_from_service(self, service_performed_id: int, spare_part_id: int):
        db_spare_part = self.db.query(ServicePerformedSparePartModel).filter(
            ServicePerformedSparePartModel.IdServicioRealizado == service_performed_id,
            ServicePerformedSparePartModel.IdRepuesto == spare_part_id
        ).first()

        if db_spare_part:
            self.db.delete(db_spare_part)
            self.db.commit()
            return True
        return False