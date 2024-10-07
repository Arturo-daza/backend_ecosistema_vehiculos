from sqlalchemy.orm import Session
from models.preventive_maintenance import PreventiveMaintenance as PreventiveMaintenanceModel
from schemas.preventive_maintenance import PreventiveMaintenanceCreate, PreventiveMaintenanceUpdate

class PreventiveMaintenanceService:
    def __init__(self, db: Session):
        self.db = db

    def get_maintenance(self, maintenance_id: int):
        return self.db.query(PreventiveMaintenanceModel).filter(PreventiveMaintenanceModel.IdMantenimientoPreventivo == maintenance_id).first()

    def get_maintenances_by_vehicle(self, vehicle_id: str):
        return self.db.query(PreventiveMaintenanceModel).filter(PreventiveMaintenanceModel.IdVehiculo == vehicle_id).all()

    def create_maintenance(self, maintenance: PreventiveMaintenanceCreate):
        db_maintenance = PreventiveMaintenanceModel(**maintenance.dict())
        self.db.add(db_maintenance)
        self.db.commit()
        self.db.refresh(db_maintenance)
        return db_maintenance

    def update_maintenance(self, maintenance_id: int, maintenance: PreventiveMaintenanceUpdate):
        db_maintenance = self.get_maintenance(maintenance_id)
        if not db_maintenance:
            return None
        for key, value in maintenance.dict(exclude_unset=True).items():
            setattr(db_maintenance, key, value)
        self.db.commit()
        self.db.refresh(db_maintenance)
        return db_maintenance

    def delete_maintenance(self, maintenance_id: int):
        db_maintenance = self.get_maintenance(maintenance_id)
        if not db_maintenance:
            return False
        self.db.delete(db_maintenance)
        self.db.commit()
        return True
