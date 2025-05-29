from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.staticfiles import StaticFiles
import logging
from fastapi.middleware.cors import CORSMiddleware

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite dev server default
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/assets", StaticFiles(directory="web-app/assets"), name="assets")

@app.get("/")
def iniciando_sesion():
    return FileResponse("web-app/index.html")

from Routers import estudiantes, constancias, solicitudes, login


# app.include_router(login.router, prefix="/v1/login", tags=["Login"])
app.include_router(estudiantes.router, prefix="/v1/estudiantes", tags=["Estudiantes"])
app.include_router(constancias.router, prefix="/v1/constancias", tags=["Constancias"])
app.include_router(solicitudes.router, prefix="/v1/solicitudes", tags=["Solicitudes"])


