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
from routers.file import file_router
from routers.preventive_maintenance import preventive_maintenance_router


app  = FastAPI()
app.title = "Documentación Ecosistema Digital de vehículos"
app.version= "0.0.1"

app.add_middleware(ErrorHandler)
app.include_router(user_router, prefix="/api/user", tags=["users"])
app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(vehicle_router, prefix="/api/vehicle", tags=["vehicles"])
app.include_router(service_router, prefix="/api/service", tags=["services"])
app.include_router(custom_service_router, prefix="/api/custom_service", tags=["services"])
app.include_router(location_router, prefix="/api/location", tags=["location"])
app.include_router(sparepart_router, prefix="/api/sparepart", tags=["sparepart"])
app.include_router(service_performed_router, prefix="/api/service/history", tags=["service history"])
app.include_router(file_router, prefix="/api/file", tags=["file"])
app.include_router(preventive_maintenance_router, prefix="/api/maintenance", tags=["preventive maintenance"])


@app.get('/', tags=["home"])
def message():
    return HTMLResponse("<H1> I Love YOU My Live </H1>")
  


