from fastapi.security import HTTPBearer
from fastapi import Request, HTTPException
from utils.jwt_manager import validate_token

class JWTBearer(HTTPBearer):
    """
    Clase para la verificación de tokens JWT en las rutas protegidas.
    """
    async def __call__(self, request: Request):
        # Obtener las credenciales del encabezado Authorization
        auth = await super().__call__(request)

        # Validar el token y extraer los datos
        data = validate_token(auth.credentials)
        
        # Aquí puedes agregar más validaciones según sea necesario
        # Por ejemplo, validación de roles, permisos, etc.
        if 'email' not in data:
            raise HTTPException(status_code=403, detail="Credenciales inválidas")

        return data  # Retornar los datos para que puedan ser utilizados en las rutas protegidas
