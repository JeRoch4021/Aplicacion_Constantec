import inspect
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from fastapi.staticfiles import StaticFiles

from database.connection import close_database_connection, engine
from database.initialize_database import (
    create_admin_user,
    create_database,
    create_tables_in_database,
)
from sqladmin import Admin
import admin as AdminViews

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

admin = Admin(app, engine, base_url='/admin')

for attribute_name in AdminViews.__all__:
        attribute_value = getattr(AdminViews, attribute_name)
        if inspect.isclass(attribute_value):
            admin.add_view(attribute_value)

app.mount("/assets", StaticFiles(directory="web-app/assets"), name="assets")

# app.include_router(login.router, prefix="/v1/login", tags=["Login"])
# app.include_router(estudiantes.router, prefix="/v1/estudiantes", tags=["Estudiantes"])
# app.include_router(constancias.router, prefix="/v1/constancias", tags=["Constancias"])
# app.include_router(solicitudes.router, prefix="/v1/solicitudes", tags=["Solicitudes"])

@app.get("/{full_path:path}")
def web_app(full_path: str):
    if full_path.startswith("v1"):
        raise HTTPException(status_code=404, detail="Not Found")
    return FileResponse("web-app/index.html")
