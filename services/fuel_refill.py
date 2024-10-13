from datetime import datetime
from sqlalchemy.orm import Session
from models.fuel_refill import FuelRefill as FuelRefillModel
from schemas.fuel_refill import FuelRefillCreate
from models.vehicle import Vehicle as VehicleModel
class FuelRefillService:
    def __init__(self, db: Session):
        self.db = db

    def create_fuel_refill(self, refill: FuelRefillCreate):
        # Calcular el costo total
        costo_total = refill.GalonesTanqueados * refill.PrecioGalon
        db_refill = FuelRefillModel(
            IdVehiculo=refill.IdVehiculo,
            Fecha = refill.Fecha,
            Kilometraje=refill.Kilometraje,
            GalonesTanqueados=refill.GalonesTanqueados,
            TipoCombustible=refill.TipoCombustible,
            PrecioGalon=refill.PrecioGalon,
            CostoTotal=costo_total,
            EstacionServicio=refill.EstacionServicio,
            IdUbicacion=refill.IdUbicacion
        )
        self.db.add(db_refill)
        self.db.commit()
        self.db.refresh(db_refill)
        return db_refill

    def get_fuel_refill(self, refill_id: int):
        return self.db.query(FuelRefillModel).filter(FuelRefillModel.IdRecargaCombustible == refill_id).first()

    def get_fuel_refills_by_vehicle(self, vehicle_id: str):
        return self.db.query(FuelRefillModel).filter(FuelRefillModel.IdVehiculo == vehicle_id).all()

    def delete_fuel_refill(self, refill_id: int):
        db_refill = self.get_fuel_refill(refill_id)
        if db_refill:
            self.db.delete(db_refill)
            self.db.commit()
            return True
        return False
    
    def get_fuel_refills_by_user(self, user_id: int):
        # Realizamos un JOIN entre las tablas Vehiculo y RecargaCombustible
        query = (
            self.db.query(FuelRefillModel)
            .join(VehicleModel, VehicleModel.Placa == FuelRefillModel.IdVehiculo)
            .filter(VehicleModel.IdUsuario == user_id)
        )

        # Ejecutamos la consulta y obtenemos todas las recargas de combustible asociadas a los vehículos del usuario
        fuel_refills = query.all()

        return fuel_refills

    