from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.user import User as UserModel
from schemas.user import UserUpdate, User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    def __init__(self, db: Session): 
        self.db = db
        
    def verify_password(self, plain_password, hashed_password):
        """
        Verifica si la contraseña proporcionada coincide con la almacenada.
        """
        return pwd_context.verify(plain_password, hashed_password)

    def get_user_by_email(self, email: str):
            return self.db.query(UserModel).filter(UserModel.Email == email).first()

    def get_user(self, user_id: int):
        return self.db.query(UserModel).filter(User.IdUsuario == user_id).first()

    def get_users(self, skip: int = 0, limit: int = 100):
        return self.db.query(UserModel).offset(skip).limit(limit).all()
    
    def hash_password(self, plain_password: str) -> str:
        """
        Hash the password using bcrypt.
        """
        return pwd_context.hash(plain_password)

    # Método para verificar si la contraseña está hasheada
    def is_hashed(self, password: str) -> bool:
        return password.startswith('$2b$')  # Comprobación básica para bcrypt
    
    def create_user(self, user: User):
        # Validar si el correo ya existe
        if self.get_user_by_email(user.Email):
            raise HTTPException(status_code=400, detail="El correo ya está registrado")
        elif self.get_user_by_email(user.NumeroDocumento):
            raise HTTPException(status_code=400, detail="El Documento ya está registrado")
        
        # Hashear la contraseña antes de almacenarla
        hashed_password = self.hash_password(user.Contrasena)
        user_data = user.model_dump()
        user_data['Contrasena'] = hashed_password  # Reemplaza la contraseña con la hasheada

        db_user = UserModel(**user_data)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def update_user(self, user_id: int, user: UserUpdate):
        db_user = self.db.query(UserModel).filter(UserModel.IdUsuario == user_id).first()
        print(user)
        
        if db_user:
            for var, value in user.dict(exclude_unset=True).items():
                if var == "Contrasena":  # Validar la contraseña
                    if not self.is_hashed(value):  # Si no está hasheada
                        value = self.hash_password(value)
                
                setattr(db_user, var, value)
                
            self.db.commit()
            self.db.refresh(db_user)
            return db_user
        else:
            return None

    def delete_user(self, user_id: int):
        db_user = self.db.query(UserModel).filter(UserModel.IdUsuario == user_id).first()
        if db_user:
            self.db.delete(db_user)
            self.db.commit()
            return True
        else:
            return False

    def get_user_by_document(self, document_number: str):
        return self.db.query(UserModel).filter(User.NumeroDocumento == document_number).first()

    def get_user_by_phone(self, phone_number: str):
        return self.db.query(UserModel).filter(User.Telefono == phone_number).first()

    def get_user_by_role(self, role_id: int):
        return self.db.query(UserModel).filter(User.IdRol == role_id).all()

    def get_user_by_type(self, user_type: str):
        return self.db.query(UserModel).filter(User.TipoUsuario == user_type).all()