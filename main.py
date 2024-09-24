from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from schemas.user import User
from middlewares.error_handler import ErrorHandler
from routers.user import user_router
from routers.auth import auth_router


app  = FastAPI()
app.title = "Documentación Ecosistema Digital de vehículos"
app.version= "0.0.1"

app.add_middleware(ErrorHandler)
app.include_router(user_router, prefix="/user", tags=["users"])
app.include_router(auth_router, prefix="/auth", tags=["auth"])
# app.include_router(movie_router)


@app.get('/', tags=["home"])
def message():
    return HTMLResponse("<H1> HELLO </H1>")
  


