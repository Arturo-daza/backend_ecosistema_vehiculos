from sqlalchemy.orm import Session
from models.service_performed import ServicePerformed as ServicePerformedModel
from schemas.service_performed import ServicePerformedCreate

class ServicePerformedService:
    def __init__(self, db: Session):
        self.db = db

    def get_service_performed(self, service_performed_id: int):
        return self.db.query(ServicePerformedModel).filter(ServicePerformedModel.IdServicioRealizado == service_performed_id).first()

    def get_services_performed(self, skip: int = 0, limit: int = 100):
        return self.db.query(ServicePerformedModel).offset(skip).limit(limit).all()

    def create_service_performed(self, service_performed: ServicePerformedCreate):
        db_service_performed = ServicePerformedModel(**service_performed.dict())
        self.db.add(db_service_performed)
        self.db.commit()
        self.db.refresh(db_service_performed)
        return db_service_performed

    def delete_service_performed(self, service_performed_id: int):
        service_performed = self.get_service_performed(service_performed_id)
        if service_performed:
            self.db.delete(service_performed)
            self.db.commit()
            return True
        return False
