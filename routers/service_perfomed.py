from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.database import Database
from schemas.service_performed import ServicePerformedCreate, ServicePerformed
from services.service_performed import ServicePerformedService
from middlewares.jwt_bearer import JWTBearer
from schemas.user import User as UserSchema
from dependencies.validate_user_access import validate_user_access


service_performed_router = APIRouter()

get_db = Database.get_instance().get_db

@service_performed_router.post("/",  response_model=ServicePerformed, dependencies=[Depends(JWTBearer())]
)
def create_service_performed(service_performed: ServicePerformedCreate, db: Session = Depends(get_db)):
    service = ServicePerformedService(db)
    return service.create_service_performed(service_performed)

@service_performed_router.get("/{service_performed_id}", response_model=ServicePerformed, dependencies=[Depends(JWTBearer())]
)
def get_service_performed(service_performed_id: int, db: Session = Depends(get_db), current_user: UserSchema = Depends(validate_user_access)
):
    service = ServicePerformedService(db)
    result = service.get_service_performed(service_performed_id)
    if not result:
        raise HTTPException(status_code=404, detail="Service performed not found")
    return result

@service_performed_router.delete("/{service_performed_id}", dependencies=[Depends(JWTBearer())]
)
def delete_service_performed(service_performed_id: int, db: Session = Depends(get_db), current_user: UserSchema = Depends(validate_user_access)
):
    service = ServicePerformedService(db)
    if not service.delete_service_performed(service_performed_id):
        raise HTTPException(status_code=404, detail="Service performed not found")
    return {"message": "Service performed deleted successfully"}


