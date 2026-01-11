import inspect
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.staticfiles import StaticFiles
import logging
from fastapi.middleware.cors import CORSMiddleware
from routers import estudiantes, constancias, solicitudes, login, encuestas
from sqladmin import Admin
from database.connection import engine
import admin as AdminViews

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

admin = Admin(app, engine, base_url='/admin')

for attribute_name in AdminViews.__all__:
        attribute_value = getattr(AdminViews, attribute_name)
        if inspect.isclass(attribute_value):
            admin.add_view(attribute_value)

app.mount("/assets", StaticFiles(directory="web-app/assets"), name="assets")

app.include_router(login.router, prefix="/v1/login", tags=["Login"])
app.include_router(estudiantes.router, prefix="/v1/estudiantes", tags=["Estudiantes"])
app.include_router(constancias.router, prefix="/v1/constancias", tags=["Constancias"])
app.include_router(solicitudes.router, prefix="/v1/solicitudes", tags=["Solicitudes"])
app.include_router(encuestas.router, prefix="/v1/encuestas", tags=["Encuestas"])


@app.get("/{full_path:path}")
def iniciando_sesion(full_path: str):
    if full_path.startswith("v1"):
        raise HTTPException(status_code=404, detail="Not Found")
    return FileResponse("web-app/index.html")
