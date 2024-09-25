import os
from jwt import encode, decode, exceptions
from datetime import datetime, timedelta
from fastapi import HTTPException

# Cargar la clave secreta desde variables de entorno para mayor seguridad
SECRET_KEY = os.getenv("SECRET_KEY", "my_secrete_key")

def create_token(data: dict, expires_in_minutes: int = 60) -> str:
    """
    Crea un JWT con un tiempo de expiración.
    """
    to_encode = data.copy()
    # Añadir la expiración al payload
    to_encode.update({"exp": datetime.utcnow() + timedelta(minutes=expires_in_minutes)})
    token: str = encode(payload=to_encode, key=SECRET_KEY, algorithm="HS256")
    return token

def validate_token(token: str) -> dict:
    """
    Valida y decodifica un JWT. Maneja posibles excepciones.
    """
    try:
        data: dict = decode(token, key=SECRET_KEY, algorithms=["HS256"])
        return data
    except exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except exceptions.DecodeError:
        raise HTTPException(status_code=401, detail="Token inválido")
    except exceptions.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token no válido")
