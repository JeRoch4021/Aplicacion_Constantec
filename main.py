from fastapi import FastAPI
import routers_estudiantes

app = FastAPI()

app.include_router(routers_estudiantes.router, prefix="/estudiantes", tags=["Esstudiantes"])