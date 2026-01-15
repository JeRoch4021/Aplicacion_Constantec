#from fastapi.security import OAuth2PasswordRequestForm
from fastapi import status, Response
from paquetes import schemas
from sqlalchemy.orm import Session
#from sqlalchemy.orm.exc import NoResultFound
from database.connection import SessionLocal
from fastapi import APIRouter, Depends, HTTPException
from crud import crud_estudiante
from crud import crud_administrador
from typing import Any
from autenticacion.seguridad import verify_password, create_access_token
from comun.response import Response as CommonResponse
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

# Dependencias para obtener sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=CommonResponse)
async def login_for_access_token(login_request: schemas.LoginRequest, response: Response, db: Session = Depends(get_db)):
    usuario = None
    tipo = None

    """
    Authenticates a user with username and password and returns a JWT.
    Client should send credentials as 'application/x-www-form-urlencoded'.
    """
    try: 
        if login_request.usuario.isdigit():
            usuario = crud_estudiante.obtener_estudiante_por_no_control(db, login_request.usuario)
            tipo = "estudiante" if usuario else None
        else:
            usuario = crud_administrador.obtener_administrador_por_id(db, login_request.usuario)
            tipo = "admin" if usuario else None
        
        if usuario is None:
            raise HTTPException (detail="Usuario no encontrado", status_code=status.HTTP_404_NOT_FOUND)
        
        logging.debug(usuario.password)
        if not verify_password(login_request.password, usuario.password):
            raise HTTPException (detail="Password incorrecto", status_code=status.HTTP_401_UNAUTHORIZED)

    except Exception as ex:
        raise ex

    # 3. User is authenticated, create the JWT
    # You can include additional data in the token if needed (the 'sub' claim is standard for subject/username)
    access_token_payload = {
        "sub": login_request.usuario,
        "tipo": tipo,
    }
    access_token = create_access_token(jwt_payload=access_token_payload)

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        path="/"
    )
    
    # Devolvemos la respuesta, comprobando si es un administrador
    return CommonResponse(
        data = {"token" : access_token,
                "estudiante_id": usuario.id,
                "tipo" : tipo}, 
                success= True, 
                messsage="autenticacion exitosa", 
                error_code= None)