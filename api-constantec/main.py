import inspect
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.staticfiles import StaticFiles
import logging
from fastapi.middleware.cors import CORSMiddleware
from routers import estudiantes, constancias, solicitudes, login, encuestas
from sqladmin import Admin
from starlette.requests import Request
from starlette.responses import RedirectResponse
from autenticacion.seguridad import decode_access_token
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

class AdminAutenticador:
     async def login(self, request: Request) -> bool:
        return False
     
     async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True
     
     async def authenticate(self, request: Request) -> bool:
        token = request.cookies.get("admin_token")
        if token:
            payload = decode_access_token(token)
            if payload and payload.get("tipo") == "admin":
                return True
        return False

admin = Admin(app, engine, base_url='/admin-panel')

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

@app.get("/admin-access")
async def acceso_administrador(token: str = None):
    if not token:
        raise HTTPException(status_code=401, detail="Token requerido")
    payload = decode_access_token(token)
    if not payload or payload.get("tipo") != "admin":
        raise HTTPException(status_code=403, detail="No autorizado")
    response = RedirectResponse(url="/admin-panel", status_code=302)
    response.set_cookie("admin_token", token, httponly=True)
    return response
