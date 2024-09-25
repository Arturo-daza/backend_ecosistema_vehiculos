from pydantic import BaseModel, EmailStr

class RecoverPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str