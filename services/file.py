import os
from sqlalchemy.orm import Session
from models.file import File as FileModel
from schemas.file import FileCreate
from utils.digital_ocean_spaces import DigitalOceanSpaces

class FileService:
    def __init__(self, db: Session):
        self.db = db
        self.storage = DigitalOceanSpaces()

    def upload_file(self, file: FileCreate, file_path: str):
        # Upload file to DigitalOcean Spaces
        file_url = self.storage.upload_file(file_path, file.NombreArchivo)
        
        if "http" not in file_url:
            return file_url  # Error message
        
        # Save file details in the database
        file.Ruta = file_url
        db_file = FileModel(**file.dict())
        self.db.add(db_file)
        self.db.commit()
        self.db.refresh(db_file)
        
        return db_file

    def delete_file(self, file_id: int):
        # Get the file from the database
        db_file = self.db.query(FileModel).filter(FileModel.IdArchivo == file_id).first()
        if not db_file:
            return None
        
        # Delete file from DigitalOcean Spaces
        self.storage.delete_file(db_file.NombreArchivo)
        
        # Delete file from the database
        self.db.delete(db_file)
        self.db.commit()
        
        return db_file

    def get_file(self, file_id: int):
        return self.db.query(FileModel).filter(FileModel.IdArchivo == file_id).first()