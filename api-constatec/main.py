from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from Routers import estudiantes, constancias, solicitudes, login
from sqlalchemy.orm import Session
from Database.database import SessionLocal
from CRUD import crud_estudiante
from Schemas import schemas

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def iniciando_sesion():
    return {"mensaje": "API de constancias activa. Usa /docs para ver la documentacion. :)"}

# app.include_router(login.router, prefix="/v1/login", tags=["Login"])
app.include_router(estudiantes.router, prefix="/v1/estudiantes", tags=["Estudiantes"])
app.include_router(constancias.router, prefix="/v1/constancias", tags=["Constancias"])
app.include_router(solicitudes.router, prefix="/v1/solicitudes", tags=["Solicitudes"])


