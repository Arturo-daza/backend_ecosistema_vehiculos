from sqlalchemy.orm import Session
from models.tem_service_performed import TempServicePerformed as TempServicePerformedModel
from schemas.tem_service_performed import TempServicePerformedCreate, TempServicePerformedUpdate
from models.vehicle import Vehicle as VehicleModel

class TempServicePerformedService:
    def __init__(self, db: Session):
        self.db = db

    def create_service_performed(self, service_performed_data: TempServicePerformedCreate):
        db_service_performed = TempServicePerformedModel(**service_performed_data.dict())
        self.db.add(db_service_performed)
        self.db.commit()
        self.db.refresh(db_service_performed)
        return db_service_performed

    def get_service_performed(self, service_performed_id: int):
        return self.db.query(TempServicePerformedModel).filter(TempServicePerformedModel.IdServicioRealizado == service_performed_id).first()

    def get_services_by_vehicle(self, placa_vehiculo: str):
        return self.db.query(TempServicePerformedModel).filter(TempServicePerformedModel.PlacaVehiculo == placa_vehiculo).all()

    def delete_service_performed(self, service_performed_id: int):
        db_service_performed = self.get_service_performed(service_performed_id)
        if db_service_performed:
            self.db.delete(db_service_performed)
            self.db.commit()
            return True
        return False
    def get_services_by_user(self, user_id: int):
        # Obtener los vehículos asociados al usuario
        vehicles = self.db.query(VehicleModel).filter(VehicleModel.IdUsuario == user_id).all()

        # Obtener todos los servicios realizados para los vehículos del usuario
        services = []
        for vehicle in vehicles:
            vehicle_services = self.db.query(TempServicePerformedModel).filter(TempServicePerformedModel.PlacaVehiculo == vehicle.Placa).all()
            services.extend(vehicle_services)

        return services
    
    def get_business_concepts_spareparts(self, user_id: int):
        # Obtener vehículos del usuario
        vehicles = self.db.query(VehicleModel).filter(VehicleModel.IdUsuario == user_id).all()

        if not vehicles:
            return {"negocios": [], "conceptos": [], "repuestos": []}

        # Obtener todos los servicios realizados por los vehículos del usuario
        vehicle_plates = [v.Placa for v in vehicles]
        services = self.db.query(TempServicePerformedModel).filter(TempServicePerformedModel.PlacaVehiculo.in_(vehicle_plates)).all()

        # Listas para almacenar los negocios, conceptos y repuestos únicos
        negocios = set()
        conceptos = set()
        repuestos = set()

        for service in services:
            # Negocios vinculados
            if service.NombreNegocio:
                negocios.add(service.NombreNegocio)

            # Conceptos vinculados (para talleres)
            if service.TipoServicio == 'Taller' and service.Concepto:
                conceptos.add(service.Concepto)

            # Repuestos vinculados (para talleres)
            if service.TipoServicio == 'Taller' and service.Repuestos:
                repuestos.update(service.Repuestos.split(','))  # Dividimos los repuestos si están separados por comas

        return {
            "negocios": list(negocios),
            "conceptos": list(conceptos),
            "repuestos": list(repuestos)
        }
    def update_service_performed(self, service_performed_id: int, service_performed_data: TempServicePerformedUpdate):
        # Obtener el servicio realizado por ID
        db_service_performed = self.get_service_performed(service_performed_id)
        if not db_service_performed:
            return None

        # Actualizar los campos solo si se proporcionaron nuevos valores
        update_data = service_performed_data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_service_performed, key, value)

        self.db.commit()
        self.db.refresh(db_service_performed)
        return db_service_performed