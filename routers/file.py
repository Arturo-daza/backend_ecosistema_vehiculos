import uuid
from fastapi import APIRouter, Depends, UploadFile, File as FastAPIFile, HTTPException
from sqlalchemy.orm import Session
from config.database import Database
from dependencies.get_current_user import get_current_user
from dependencies.validate_user_access import validate_user_access
from middlewares.jwt_bearer import JWTBearer
from schemas.file import FileCreate, FileResponse
from services.file import FileService
from models.file import File as FileModel
from schemas.user import User as UserSchema


import shutil
import os

file_router = APIRouter()

get_db = Database.get_instance().get_db

@file_router.post("/", response_model=FileResponse)
def upload_file(file: UploadFile = FastAPIFile(...), tipo_entidad: str = "default", db: Session = Depends(get_db)):
    file_service = FileService(db)
    
    # Generar un identificador único (UUID)
    unique_id = str(uuid.uuid4())
    
    # Extraer la extensión del archivo original
    file_extension = os.path.splitext(file.filename)[1]
    
    # Generar el nuevo nombre del archivo con el UUID
    new_filename = f"{os.path.splitext(file.filename)[0]}_{unique_id}{file_extension}"
    
    # Ruta temporal para almacenar el archivo subido
    temp_file_path = f"/tmp/{new_filename}"
    
    # Guardar el archivo temporalmente
    with open(temp_file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Preparar los metadatos del archivo para la base de datos
    file_create = FileCreate(
        NombreArchivo=new_filename,  # Usar el nuevo nombre con el UUID
        TipoArchivo=file.content_type,
        Extension=file_extension,
        Tamaño=os.path.getsize(temp_file_path),
        IdUsuarioSubida="10",  # Este valor probablemente debas obtenerlo dinámicamente
        TipoEntidad=tipo_entidad,
        Ruta=""  # Esto se completará después de subir el archivo
    )
    
    # Subir el archivo y registrarlo en la base de datos
    uploaded_file = file_service.upload_file(file_create, temp_file_path)
    
    # Limpiar el archivo temporal
    os.remove(temp_file_path)
    
    if not isinstance(uploaded_file, FileModel):
        raise HTTPException(status_code=400, detail=uploaded_file)
    
    return uploaded_file

@file_router.delete("/{file_id}", response_model=FileResponse, dependencies=[Depends(JWTBearer())])
def delete_file(file_id: int, db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    file_service = FileService(db)
    db_file = file_service.delete_file(file_id)
    
    if not db_file:
        raise HTTPException(status_code=404, detail="File not found")
    
    return db_file

@file_router.get("/{file_id}", response_model=FileResponse, dependencies=[Depends(JWTBearer())])
def get_file(file_id: int, db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    file_service = FileService(db)
    
    # Obtener archivo desde la base de datos
    db_file = file_service.get_file(file_id)
    print(db_file)
    
    if not db_file:
        raise HTTPException(status_code=404, detail="File not found")
    
    # Obtener la URL del archivo desde el servicio de almacenamiento (DigitalOcean Spaces)
    file_url = file_service.storage.get_file_url(db_file.NombreArchivo)
    print(file_url)
    
    # Retornar la URL del archivo junto con los metadatos del archivo almacenado en la base de datos
    return db_file
