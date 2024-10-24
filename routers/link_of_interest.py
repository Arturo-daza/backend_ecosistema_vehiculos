from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.database import Database
from schemas.link_of_interest import LinkOfInterestCreate, LinkOfInterestUpdate, LinkOfInterest
from services.link_of_interest import LinkOfInterestService
from middlewares.jwt_bearer import JWTBearer

link_of_interest_router = APIRouter()

get_db = Database.get_instance().get_db

# Crear un enlace de interés
@link_of_interest_router.post("/", response_model=LinkOfInterest, dependencies=[Depends(JWTBearer())])
def create_link(link: LinkOfInterestCreate, db: Session = Depends(get_db)):
    link_service = LinkOfInterestService(db)
    return link_service.create_link(link)

# Obtener un enlace de interés por ID
@link_of_interest_router.get("/{link_id}", response_model=LinkOfInterest, dependencies=[Depends(JWTBearer())])
def get_link(link_id: int, db: Session = Depends(get_db)):
    link_service = LinkOfInterestService(db)
    db_link = link_service.get_link(link_id)
    if not db_link:
        raise HTTPException(status_code=404, detail="Enlace no encontrado")
    return db_link

# Obtener todos los enlaces de interés
@link_of_interest_router.get("/", response_model=list[LinkOfInterest], dependencies=[Depends(JWTBearer())])
def get_all_links(db: Session = Depends(get_db)):
    link_service = LinkOfInterestService(db)
    return link_service.get_all_links()

# Actualizar un enlace de interés
@link_of_interest_router.put("/{link_id}", response_model=LinkOfInterest, dependencies=[Depends(JWTBearer())])
def update_link(link_id: int, link: LinkOfInterestUpdate, db: Session = Depends(get_db)):
    link_service = LinkOfInterestService(db)
    updated_link = link_service.update_link(link_id, link)
    if not updated_link:
        raise HTTPException(status_code=404, detail="Enlace no encontrado")
    return updated_link

# Eliminar un enlace de interés
@link_of_interest_router.delete("/{link_id}", dependencies=[Depends(JWTBearer())])
def delete_link(link_id: int, db: Session = Depends(get_db)):
    link_service = LinkOfInterestService(db)
    success = link_service.delete_link(link_id)
    if not success:
        raise HTTPException(status_code=404, detail="Enlace no encontrado")
    return {"message": "Enlace eliminado exitosamente"}
