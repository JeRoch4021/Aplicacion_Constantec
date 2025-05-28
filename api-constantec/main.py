from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import FileResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.staticfiles import StaticFiles

from sqlalchemy.orm import Session
# from Database.database import SessionLocal
# from CRUD import crud_estudiante
# from Schemas import schemas
from Database.init_db import init_db
from contextlib import asynccontextmanager
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

logger = logging.getLogger(__name__)

app = FastAPI()

app.mount("/assets", StaticFiles(directory="web-app/assets"), name="assets")

# def get_db():
#     db = SessionLocal()    
#     try:
#         yield db
#     finally:
#         db.close()


@app.get("/")
def iniciando_sesion():
    return FileResponse("web-app/index.html")
    # return {"mensaje": "API de constancias activa. Usa /docs para ver la documentacion. :)"}

from Routers import estudiantes, constancias, solicitudes, login


# app.include_router(login.router, prefix="/v1/login", tags=["Login"])
app.include_router(estudiantes.router, prefix="/v1/estudiantes", tags=["Estudiantes"])
app.include_router(constancias.router, prefix="/v1/constancias", tags=["Constancias"])
app.include_router(solicitudes.router, prefix="/v1/solicitudes", tags=["Solicitudes"])


