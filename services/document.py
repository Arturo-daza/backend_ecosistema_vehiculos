from sqlalchemy.orm import Session
from models.document import Document as DocumentModel
from schemas.document import DocumentCreate, DocumentUpdate
from models.vehicle import Vehicle as VehicleModel

class DocumentService:
    def __init__(self, db: Session):
        self.db = db

    def create_document(self, document_data: DocumentCreate):
        db_document = DocumentModel(**document_data.dict())
        self.db.add(db_document)
        self.db.commit()
        self.db.refresh(db_document)
        return db_document

    def get_document(self, document_id: int):
        return self.db.query(DocumentModel).filter(DocumentModel.IdDocumento == document_id).first()

    def get_documents_by_vehicle(self, vehicle_id: str):
        return self.db.query(DocumentModel).filter(DocumentModel.IdVehiculo == vehicle_id).all()

    def update_document(self, document_id: int, document_data: DocumentUpdate):
        db_document = self.get_document(document_id)
        if not db_document:
            return None

        update_data = document_data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_document, key, value)

        self.db.commit()
        self.db.refresh(db_document)
        return db_document

    def delete_document(self, document_id: int):
        db_document = self.get_document(document_id)
        if db_document:
            self.db.delete(db_document)
            self.db.commit()
            return True
        return False
    
    def get_documents_by_user(self, user_id: int):
        # Obtener los vehículos del usuario
        vehicles = self.db.query(VehicleModel).filter(VehicleModel.IdUsuario == user_id).all()
        if not vehicles:
            return []

        # Obtener todas las placas de los vehículos del usuario
        vehicle_plates = [vehicle.Placa for vehicle in vehicles]

        # Obtener todos los documentos asociados a los vehículos del usuario
        documents = self.db.query(DocumentModel).filter(DocumentModel.IdVehiculo.in_(vehicle_plates)).all()

        return documents
