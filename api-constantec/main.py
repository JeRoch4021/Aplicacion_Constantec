import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

# from fastapi_admin.app import app as admin_app
from fastapi.staticfiles import StaticFiles

from database.connection import close_database_connection, engine
from database.initialize_database import (
    create_admin_user,
    create_database,
    create_tables_in_database,
)
from models.admin import AdminUser

logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s:     %(message)s -> [%(name)s - %(asctime)s]",
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Constantec API Server starting...")
    await create_database()
    await create_tables_in_database()
    await create_admin_user()

    yield

    logger.info("Constantec API Server shutting down...")
    await close_database_connection()


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

# login_provider = UsernamePasswordProvider(
#     admin_model=AdminUser, # Your SQLAlchemy AdminUser model
#     login_logo_url="https://preview.tabler.io/static/logo.svg" # Optional
# )

# admin_app.init(
#     admin_secret="your_strong_secret_key", # Change this!
#     permission=True,
#     site_name="My FastAPI Admin",
#     admin_model=AdminUser, # Crucial for SQLAlchemy
#     engine=engine, # Pass your SQLAlchemy async engine
#     login_provider=login_provider,
#     # resources=[UserAdmin] # This is one way, or use @admin_app_instance.register
# )

# app.mount("/admin", app=admin_app)


@app.get("/{full_path:path}")
def iniciando_sesion(full_path: str):
    if full_path.startswith("v1"):
        raise HTTPException(status_code=404, detail="Not Found")
    return FileResponse("web-app/index.html")
