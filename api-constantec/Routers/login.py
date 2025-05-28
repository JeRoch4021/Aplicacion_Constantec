from fastapi.security import OAuth2PasswordRequestForm
from fastapi import status
from Schemas import schemas
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from Database.database import SessionLocal
from fastapi import APIRouter, Depends, HTTPException
from CRUD import crud_estudiante
from typing import Any
from Autenticacion.seguridad import verify_password, create_access_token
from Comun.response import Response

router = APIRouter()

# Dependencias para obtener sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=Response)
async def login_for_access_token(estudiante_login: schemas.EstudiantesLogin, db: Session = Depends(get_db)):
    """
    Authenticates a user with username and password and returns a JWT.
    Client should send credentials as 'application/x-www-form-urlencoded'.
    """
    # user = get_user_from_db(form_data.username)
    try: 
        estudiante = crud_estudiante.obtener_estudiante_por_no_control(db, estudiante_login.No_Control)
        if estudiante is None:
            
            raise HTTPException (detail="Usuario no encontrado", status_code=status.HTTP_404_NOT_FOUND)

        if not verify_password(estudiante_login.Contrasena, estudiante.Contrasena):
            raise HTTPException (detail="Password incorrecto", status_code=status.HTTP_401_UNAUTHORIZED)
        
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
    access_token_payload = {
        "sub": estudiante.No_Control,
        "name": estudiante.Nombre
    }
    access_token = create_access_token(jwt_payload=access_token_payload)
    return Response(data=dict(token= access_token), success= True, messsage="autenticacion exitosa", error_code= None)


# Example of a protected endpoint (you'll need to implement token verification for this)
# @app.get("/users/me")
# async def read_users_me():
#     # This is just a placeholder.
#     # You would add a dependency here to verify the JWT sent by the client.
#     # See the previous comprehensive JWT example for how to create `get_current_user`.
#     return {"message": "This endpoint would show current user data if token is valid."}

# #