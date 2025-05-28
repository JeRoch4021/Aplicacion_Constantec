from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import FileResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.staticfiles import StaticFiles
from Routers import estudiantes, constancias, solicitudes, login
from sqlalchemy.orm import Session
from Database.database import SessionLocal
from CRUD import crud_estudiante
from Schemas import schemas

app = FastAPI()

app.mount("/assets", StaticFiles(directory="web-app/assets"), name="assets")

# @app.get("/app")
# async def serve_vue(full_path: str):
#     return FileResponse("web-app/index.html")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def iniciando_sesion():
    return FileResponse("web-app/index.html")
    # return {"mensaje": "API de constancias activa. Usa /docs para ver la documentacion. :)"}

# app.include_router(login.router, prefix="/v1/login", tags=["Login"])
app.include_router(estudiantes.router, prefix="/v1/estudiantes", tags=["Estudiantes"])
app.include_router(constancias.router, prefix="/v1/constancias", tags=["Constancias"])
app.include_router(solicitudes.router, prefix="/v1/solicitudes", tags=["Solicitudes"])


