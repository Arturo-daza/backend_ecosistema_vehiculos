from sqlalchemy.orm import Session
from models.customService import CustomService as CustomServiceModel
from schemas.customService import CustomServiceCreate, CustomServiceUpdate

class CustomServiceService:
    def __init__(self, db: Session):
        self.db = db

    def get_custom_service(self, custom_service_id: int):
        return self.db.query(CustomServiceModel).filter(CustomServiceModel.IdServicioPersonalizado == custom_service_id).first()

    def get_custom_services(self, skip: int = 0, limit: int = 100):
        return self.db.query(CustomServiceModel).offset(skip).limit(limit).all()

    def create_custom_service(self, custom_service: CustomServiceCreate):
        db_custom_service = CustomServiceModel(**custom_service.model_dump())
        self.db.add(db_custom_service)
        self.db.commit()
        self.db.refresh(db_custom_service)
        return db_custom_service

    def update_custom_service(self, custom_service_id: int, custom_service: CustomServiceUpdate):
        db_custom_service = self.db.query(CustomServiceModel).filter(CustomServiceModel.IdServicioPersonalizado == custom_service_id).first()
        if db_custom_service:
            for var, value in custom_service.model_dump(exclude_unset=True).items():
                setattr(db_custom_service, var, value)
            self.db.commit()
            self.db.refresh(db_custom_service)
            return db_custom_service
        return None

    def delete_custom_service(self, custom_service_id: int):
        db_custom_service = self.db.query(CustomServiceModel).filter(CustomServiceModel.IdServicioPersonalizado == custom_service_id).first()
        if db_custom_service:
            self.db.delete(db_custom_service)
            self.db.commit()
            return True
        return False
