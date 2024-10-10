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
    
    # Create a temporary file to store the uploaded content
    temp_file_path = f"/tmp/{file.filename}"
    
    
    with open(temp_file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Prepare file metadata for database
    file_create = FileCreate(
        NombreArchivo=file.filename,
        TipoArchivo=file.content_type,
        Extension=os.path.splitext(file.filename)[1],
        Tamaño=os.path.getsize(temp_file_path),
        IdUsuarioSubida="10",
        TipoEntidad=tipo_entidad,
        Ruta=""  # Will be filled after uploading to the space
    )
    
    # Upload file and register in the database
    uploaded_file = file_service.upload_file(file_create, temp_file_path)
    
    
    # Clean up the temporary file
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
