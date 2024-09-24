from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from schemas.user import User
from jwt_manager import create_token
from middlewares.error_handler import ErrorHandler
from routers.user import user_router
from routers.auth import auth_router


app  = FastAPI()
app.title = "Documentación Ecosistema Digital de vehículos"
app.version= "0.0.1"

app.add_middleware(ErrorHandler)
app.include_router(user_router, tags=["users"])
app.include_router(auth_router, tags=["auth"])
# app.include_router(movie_router)


@app.get('/', tags=["home"])
def message():
    return HTMLResponse("<H1> HELLO </H1>")
  
# @app.post('/login', tags=['auth'])
# def login(user: User):
#   if user.email == "admin@gmail.com" and user.password =="admin":
#     token: str = create_token(user.model_dump())
#   return JSONResponse(status_code=201, content = token)

