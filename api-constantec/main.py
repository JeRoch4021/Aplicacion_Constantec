import logging

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.staticfiles import StaticFiles
from database.initialize_database import initialize_database
from contextlib import asynccontextmanager

# from Routers import constancias, estudiantes, login, solicitudes

logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s:     %(message)s -> [%(name)s - %(asctime)s]"
)

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Constantec API Server starting...")
    await initialize_database()

    yield

    logger.info("Constantec API Server shutting down...")
    # await close_db_connection() # Example of shutdown logic
    # Add other shutdown logic here, e.g., closing connect

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite dev server default
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/assets", StaticFiles(directory="web-app/assets"), name="assets")

# app.include_router(login.router, prefix="/v1/login", tags=["Login"])
# app.include_router(estudiantes.router, prefix="/v1/estudiantes", tags=["Estudiantes"])
# app.include_router(constancias.router, prefix="/v1/constancias", tags=["Constancias"])
# app.include_router(solicitudes.router, prefix="/v1/solicitudes", tags=["Solicitudes"])


@app.get("/{full_path:path}")
def iniciando_sesion(full_path: str):
    if full_path.startswith("v1"):
        raise HTTPException(status_code=404, detail="Not Found")
    return FileResponse("web-app/index.html")
