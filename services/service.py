from sqlalchemy.orm import Session
from models.service import Service as ServiceModel
from models.customService import CustomService as CustomServiceModel
from schemas.service import ServicioCreate, ServicioUpdate

class ServiceService:
    def __init__(self, db: Session):
        self.db = db

    def get_servicio(self, servicio_id: int):
        return self.db.query(ServiceModel).filter(ServiceModel.IdServicio == servicio_id).first()

    def get_servicios(self, skip: int = 0, limit: int = 100):
        return self.db.query(ServiceModel).offset(skip).limit(limit).all()

    def create_servicio(self, servicio: ServicioCreate):
        db_servicio = ServiceModel(**servicio.dict())
        self.db.add(db_servicio)
        self.db.commit()
        self.db.refresh(db_servicio)
        return db_servicio

    def update_servicio(self, servicio_id: int, servicio: ServicioUpdate):
        db_servicio = self.db.query(ServiceModel).filter(ServiceModel.IdServicio == servicio_id).first()
        if db_servicio:
            for var, value in vars(servicio).items():
                setattr(db_servicio, var, value)
            self.db.commit()
            self.db.refresh(db_servicio)
            return db_servicio
        else:
            return None

    def delete_servicio(self, servicio_id: int):
        db_servicio = self.db.query(ServiceModel).filter(ServiceModel.IdServicio == servicio_id).first()
        if db_servicio:
            self.db.delete(db_servicio)
            self.db.commit()
            return True
        else:
            return False
        
    def get_services_by_user(self, user_id: int):
        # Realizar un JOIN entre ServicioPersonalizado y Servicio
        services = (
            self.db.query(ServiceModel)
            .join(CustomServiceModel, CustomServiceModel.IdServicio == ServiceModel.IdServicio)
            .filter(CustomServiceModel.IdUsuario == user_id)
            .all()
        )
        print(services)
        return services    
