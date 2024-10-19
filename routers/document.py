from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.database import Database
from middlewares.jwt_bearer import JWTBearer
from schemas.document import DocumentCreate, DocumentUpdate, Document
from services.document import DocumentService

document_router = APIRouter()

get_db = Database.get_instance().get_db

def documento_vencido(fecha_vencimiento: datetime) -> bool:
    # Obtener la fecha de hoy
    fecha_hoy = datetime.today().date()  # Obtén la fecha actual sin la hora
    # Comparar la fecha de vencimiento con la fecha de hoy
    if fecha_vencimiento < fecha_hoy:  # Convertir fecha_vencimiento a date
        return True
    return False

def documento_a_vencer (fecha_vencimiento: datetime) -> int:
    # Obtener la fecha de hoy
    fecha_hoy = datetime.today().date()  # Obtén la fecha actual sin la hora
    # Comparar la fecha de vencimiento con la fecha de hoy
    dias_para_vencer = (fecha_vencimiento - fecha_hoy).days
    return dias_para_vencer

# Crear un documento
@document_router.post("/", response_model=Document, dependencies=[Depends(JWTBearer())])
def create_document(document: DocumentCreate, db: Session = Depends(get_db)):
    document_service = DocumentService(db)
    db_document = document_service.create_document(document)
    db_document = db_document.__dict__.copy()
    
    if db_document["TieneFechaVencimiento"]:
        db_document["EstaVencido"] = documento_vencido(db_document["FechaVencimiento"])  # Cambia esto
        if not db_document["EstaVencido"]:
            db_document["DiasParaVencer"] = documento_a_vencer(db_document["FechaVencimiento"])
    
    return db_document

# Obtener un documento por ID
@document_router.get("/{document_id}", response_model=Document, dependencies=[Depends(JWTBearer())])
def get_document(document_id: int, db: Session = Depends(get_db)):
    document_service = DocumentService(db)
    
    db_document = document_service.get_document(document_id)
    if not db_document:
        raise HTTPException(status_code=404, detail="Documento no encontrado")
    
    db_document = db_document.__dict__.copy()  # Convierte el objeto a diccionario

    # Verifica si tiene fecha de vencimiento
    if db_document["TieneFechaVencimiento"]:
        # Asegúrate de convertir a date si es un datetime
        fecha_vencimiento = db_document["FechaVencimiento"]
        if isinstance(fecha_vencimiento, datetime):  # Verifica si es datetime
            fecha_vencimiento = fecha_vencimiento.date()  # Convierte a date
        
        db_document["EstaVencido"] = documento_vencido(fecha_vencimiento)  # Verifica si está vencido
        
        # Calcula los días para vencer solo si no está vencido
        if not db_document["EstaVencido"]:
            db_document["DiasParaVencer"] = documento_a_vencer(fecha_vencimiento)
    
    return db_document


# Actualizar un documento
@document_router.put("/{document_id}", response_model=Document, dependencies=[Depends(JWTBearer())])
def update_document(document_id: int, document: DocumentUpdate, db: Session = Depends(get_db)):
    document_service = DocumentService(db)
    updated_document = document_service.update_document(document_id, document)
    
    if not updated_document:
        raise HTTPException(status_code=404, detail="Documento no encontrado")
    
    updated_document = updated_document.__dict__.copy()  # Convierte el objeto a diccionario
    
    # Verifica si tiene fecha de vencimiento
    if updated_document["TieneFechaVencimiento"]:
        # Asegúrate de convertir a date si es un datetime
        fecha_vencimiento = updated_document["FechaVencimiento"]
        if isinstance(fecha_vencimiento, datetime):  # Verifica si es datetime
            fecha_vencimiento = fecha_vencimiento.date()  # Convierte a date
        
        updated_document["EstaVencido"] = documento_vencido(fecha_vencimiento)  # Verifica si está vencido
        
        # Calcula los días para vencer solo si no está vencido
        if not updated_document["EstaVencido"]:
            updated_document["DiasParaVencer"] = documento_a_vencer(fecha_vencimiento)

    return updated_document


# Eliminar un documento
@document_router.delete("/{document_id}", dependencies=[Depends(JWTBearer())])
def delete_document(document_id: int, db: Session = Depends(get_db)):
    document_service = DocumentService(db)
    success = document_service.delete_document(document_id)
    if not success:
        raise HTTPException(status_code=404, detail="Documento no encontrado")
    return {"message": "Documento eliminado exitosamente"}

# Obtener todos los documentos de un usuario
@document_router.get("/users/{user_id}/documents", response_model=list[Document], dependencies=[Depends(JWTBearer())])
def get_documents_by_user(user_id: int, db: Session = Depends(get_db)):
    document_service = DocumentService(db)
    documents = document_service.get_documents_by_user(user_id)
    
    if not documents:
        raise HTTPException(status_code=404, detail="No se encontraron documentos para este usuario")

    documents_list = []
    
    for doc in documents:
        doc_dict = doc.__dict__.copy()  # Convierte el objeto a diccionario

        # Verifica si tiene fecha de vencimiento
        if doc_dict["TieneFechaVencimiento"]:
            fecha_vencimiento = doc_dict["FechaVencimiento"]
            if isinstance(fecha_vencimiento, datetime):  # Verifica si es datetime
                fecha_vencimiento = fecha_vencimiento.date()  # Convierte a date
            
            doc_dict["EstaVencido"] = documento_vencido(fecha_vencimiento)  # Verifica si está vencido
            
            # Calcula los días para vencer solo si no está vencido
            if not doc_dict["EstaVencido"]:
                doc_dict["DiasParaVencer"] = documento_a_vencer(fecha_vencimiento)

        documents_list.append(doc_dict)

    return documents_list

# Obtener documentos por vehículo
@document_router.get("/vehicles/{vehicle_id}", response_model=list[Document], dependencies=[Depends(JWTBearer())])
def get_documents_by_vehicle(vehicle_id: str, db: Session = Depends(get_db)):
    document_service = DocumentService(db)
    documents = document_service.get_documents_by_vehicle(vehicle_id)
    
    if not documents:
        raise HTTPException(status_code=404, detail="No se encontraron documentos para este vehículo")

    documents_list = []

    for doc in documents:
        doc_dict = doc.__dict__.copy()  # Convierte el objeto a diccionario

        # Verifica si tiene fecha de vencimiento
        if doc_dict["TieneFechaVencimiento"]:
            fecha_vencimiento = doc_dict["FechaVencimiento"]
            if isinstance(fecha_vencimiento, datetime):  # Verifica si es datetime
                fecha_vencimiento = fecha_vencimiento.date()  # Convierte a date
            
            doc_dict["EstaVencido"] = documento_vencido(fecha_vencimiento)  # Verifica si está vencido
            
            # Calcula los días para vencer solo si no está vencido
            if not doc_dict["EstaVencido"]:
                doc_dict["DiasParaVencer"] = documento_a_vencer(fecha_vencimiento)

        documents_list.append(doc_dict)

    return documents_list
