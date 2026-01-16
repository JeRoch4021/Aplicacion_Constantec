import inspect
from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.staticfiles import StaticFiles
import logging
from fastapi.middleware.cors import CORSMiddleware
from routers import estudiantes, constancias, solicitudes, login, encuestas, comprobantes
from sqladmin import Admin
from sqladmin.authentication import AuthenticationBackend
from autenticacion.seguridad import decode_access_token, SECRET_KEY
from database.connection import engine
from starlette.requests import Request
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware
import admin as AdminViews

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(ProxyHeadersMiddleware, trusted_hosts=["*"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite dev server default
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/admin-panel/login")
def disable_sqladmin_login():
    return RedirectResponse(url="/")

@app.get("/logout")
def logout():
    response = RedirectResponse(url="/", status_code=302)

    response.delete_cookie(key="access_token", path="/")

    return response

class AdminAutenticador(AuthenticationBackend):
     async def login(self, request: Request) -> bool:
        return True
     
     async def logout(self, request: Request) -> bool:
        request.session.clear()

        response = RedirectResponse(url="/", status_code=302)

        response.delete_cookie(key="access_token", path="/")

        response.headers["Clear-Site-Data"] = '"storage", "cookies"'

        return response
     
     async def authenticate(self, request: Request) -> bool:
        token = request.cookies.get("access_token")
        if not token:
            return False
        try:
            payload = decode_access_token(token)
            if payload and payload.get("tipo") != "admin":
                return False
        except Exception:
            return False

        return True

authentication_backend = AdminAutenticador(secret_key=SECRET_KEY)

admin = Admin(
    app, 
    engine, 
    base_url='/admin-panel', 
    authentication_backend=authentication_backend
)

for attribute_name in AdminViews.__all__:
        attribute_value = getattr(AdminViews, attribute_name)
        if inspect.isclass(attribute_value):
            admin.add_view(attribute_value)

app.mount("/assets", StaticFiles(directory="web-app/assets"), name="assets")

@app.get("/admin-access")
async def acceso_administrador(token: str = None):
    if not token:
        raise HTTPException(status_code=401, detail="Token requerido")
    payload = decode_access_token(token)

    if not payload or payload.get("tipo") != "admin":
        raise HTTPException(status_code=403, detail="No autorizado")
        
    response = RedirectResponse(url="/admin-panel/", status_code=302)
    # response.set_cookie("admin_token", token, httponly=True)
    return response

app.include_router(login.router, prefix="/v1/login", tags=["Login"])
app.include_router(estudiantes.router, prefix="/v1/estudiantes", tags=["Estudiantes"])
app.include_router(constancias.router, prefix="/v1/constancias", tags=["Constancias"])
app.include_router(solicitudes.router, prefix="/v1/solicitudes", tags=["Solicitudes"])
app.include_router(encuestas.router, prefix="/v1/encuestas", tags=["Encuestas"])
app.include_router(comprobantes.router, prefix="/v1/comprobantes", tags=["Comprobantes"])

@app.get("/{full_path:path}")
def iniciando_sesion(full_path: str):
    if full_path.startswith("v1"):
        raise HTTPException(status_code=404, detail="Not Found")
    return FileResponse("web-app/index.html")

