from fastapi import FastAPI, Depends, HTTPException
from Routers import estudiantes, constancias, solicitudes
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

app.include_router(estudiantes.router, prefix="/estudiantes", tags=["Estudiantes"])
app.include_router(constancias.router, prefix="/constancias", tags=["Constancias"])
app.include_router(solicitudes.router, prefix="/solicitudes", tags=["Solicitudes"])

