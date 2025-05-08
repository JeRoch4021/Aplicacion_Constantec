from fastapi import FastAPI
from Routers import estudiantes, constancias, solicitudes

app = FastAPI()

app.include_router(estudiantes.router, prefix="/estudiantes", tags=["Esstudiantes"])
app.include_router(constancias.router, prefix="/constancias", tags=["Constancias"])
app.include_router(solicitudes.router, prefix="/solicitudes", tags=["Solicitudes"])