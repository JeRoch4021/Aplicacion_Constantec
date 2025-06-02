import logging
from typing import Any

from Autenticacion.seguridad import (
    create_access_token,
    get_password_hash,
    verify_password,
)
from Comun.response import Response
from CRUD import crud_estudiante
from database.connection import SessionLocal
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from Schemas import schemas
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

logger = logging.getLogger(__name__)

router = APIRouter()


# Dependencias para obtener sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=Response)
async def login_for_access_token(
    estudiante_login: schemas.EstudiantesLogin, db: Session = Depends(get_db)
):
    """
    Authenticates a user with username and password and returns a JWT.
    Client should send credentials as 'application/x-www-form-urlencoded'.
    """
    try:
        estudiante = crud_estudiante.obtener_estudiante_por_no_control(
            db, estudiante_login.no_control
        )
        if estudiante is None:
            raise HTTPException(
                detail="Usuario no encontrado", status_code=status.HTTP_404_NOT_FOUND
            )
        logging.debug(estudiante.contrasena)
        if not verify_password(estudiante_login.contrasena, estudiante.contrasena):
            raise HTTPException(
                detail="Password incorrecto", status_code=status.HTTP_401_UNAUTHORIZED
            )

    except Exception as ex:
        raise ex

    # 1. Check if user exists and is not disabled (optional check)
    # if not user or (hasattr(user, 'disabled') and user.disabled):
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Incorrect username or password", # Keep messages generic for security
    #         headers={"WWW-Authenticate": "Bearer"},
    #     )

    # 2. Verify the password
    # if not verify_password(form_data.password, user.hashed_password):
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Incorrect username or password",
    #         headers={"WWW-Authenticate": "Bearer"},
    #     )

    # 3. User is authenticated, create the JWT
    # You can include additional data in the token if needed (the 'sub' claim is standard for subject/username)
    access_token_payload = {"sub": estudiante.no_control, "name": estudiante.nombre}
    access_token = create_access_token(jwt_payload=access_token_payload)
    return Response(
        data=dict(token=access_token),
        success=True,
        messsage="autenticacion exitosa",
        error_code=None,
    )


# Example of a protected endpoint (you'll need to implement token verification for this)
# @app.get("/users/me")
# async def read_users_me():
#     # This is just a placeholder.
#     # You would add a dependency here to verify the JWT sent by the client.
#     # See the previous comprehensive JWT example for how to create `get_current_user`.
#     return {"message": "This endpoint would show current user data if token is valid."}

# #
