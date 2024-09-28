from sqlalchemy.orm import Session
from models.vehicle import Vehicle as VehiculoModel
from schemas.vehicle import Vehicle

class VehicleService:
    def __init__(self, db: Session): 
        self.db = db

    def create_vehiculo(self, vehiculo: Vehicle):
        db_vehiculo = VehiculoModel(**vehiculo.dict())
        self.db.add(db_vehiculo)
        self.db.commit()
        self.db.refresh(db_vehiculo)
        return db_vehiculo

    def get_vehiculo_by_placa(self, placa: str):
        return self.db.query(VehiculoModel).filter(VehiculoModel.Placa == placa).first()
    
    def get_vehicles_by_user(self, user_id:str):
        return self.db.query(VehiculoModel).filter(VehiculoModel.IdUsuario == user_id).all()
    
    def delete_vehicle(self, vehicle_id):
        vehicle = self.db.query(VehiculoModel).filter(VehiculoModel.Placa == vehicle_id).first()
        
        if vehicle:
            self.db.delete(vehicle)
            self.db.commit()
            return {"message": "Vehículo eliminado exitosamente"}
        else:
            return {"error": "No se encontró el vehículo"}
