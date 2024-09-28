from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from schemas.user import User
from middlewares.error_handler import ErrorHandler
from routers.user import user_router
from routers.auth import auth_router
from routers.vehicle import vehicle_router
from routers.service import service_router
from routers.customService import custom_service_router
from routers.location import location_router
from routers.sparepart import sparepart_router
from routers.service_perfomed import service_performed_router


app  = FastAPI()
app.title = "Documentación Ecosistema Digital de vehículos"
app.version= "0.0.1"

app.add_middleware(ErrorHandler)
app.include_router(user_router, prefix="/user", tags=["users"])
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(vehicle_router, prefix="/vehicle", tags=["vehicles"])
app.include_router(vehicle_router, prefix="/vehicle", tags=["vehicles"])
app.include_router(service_router, prefix="/service", tags=["services"])
app.include_router(custom_service_router, prefix="/custom_service", tags=["services"])
app.include_router(location_router, prefix="/location", tags=["location"])
app.include_router(sparepart_router, prefix="/sparepart", tags=["sparepart"])
app.include_router(service_performed_router, prefix="/service/history", tags=["service history"])
# app.include_router(movie_router)


@app.get('/', tags=["home"])
def message():
    return HTMLResponse("<H1> HELLO </H1>")
  


