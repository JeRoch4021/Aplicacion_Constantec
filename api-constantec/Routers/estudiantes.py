from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from Database.database import SessionLocal
from Database.init_db import init_db
from CRUD import crud_estudiante
from Schemas import schemas
from Autenticacion.seguridad import get_current_user
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

# @router.post("/login", response_model=schemas.EstudiantesSalida)
# def login(estudiante_login: schemas.EstudiantesLogin, db: Session = Depends(get_db)):
#     try:
#         estudiante = crud_estudiante.obtener_estudiante_por_no_control(db, estudiante_login.No_Control)
#         if not estudiante or not bcrypt.checkpw(
#             estudiante_login.Contrasena.encode('utf-8'), 
#             estudiante.Contrasena.encode('utf-8')
#         ):
#             raise HTTPException (detail="Credenciales invalidas", status_code=401)
#         return estudiante
#     except Exception as ex:
#         raise HTTPException (detail=f"Error al iniciar sesión: {str(ex)}", status_code=500)

@router.post("/login", response_model=Response)
async def login_estudiante(estudiante_login: schemas.EstudiantesLogin, db: Session = Depends(get_db)):
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
    
    access_token_payload = {
        "sub": estudiante.No_Control,
        "name": estudiante.Nombre
    }
    access_token = create_access_token(jwt_payload=access_token_payload)
    return Response(data=dict(token= access_token), success= True, messsage="autenticacion exitosa", error_code= None)


@router.put("/cambiar-contrasena", response_model=schemas.EstudiantesSalida)
def cambiar_contrasena(data: schemas.EstudiantesContrasenaUpdate, db: Session = Depends(get_db)):
    estudiante_actualizado = crud_estudiante.actualizar_contrasena(db, data.No_Control, data.Nueva_Contrasena)
    if not estudiante_actualizado:
        raise HTTPException (detail="Estudiante no encontrado", status_code=404)
    return estudiante_actualizado


@router.get("/{no_control}", response_model=schemas.EstudiantesSalida)
def buscar_perfil(no_control: str, db: Session = Depends(get_db), auth_user: dict[str, Any] = Depends(get_current_user)):
    estudiante = crud_estudiante.obtener_estudiante_por_no_control(db, no_control)
    if not estudiante:
        raise HTTPException (detail="Estudiante no encontrado", status_code=404)
    
    if estudiante.No_Control != auth_user.get("sub"):
        raise HTTPException (detail="No de control no coincide con el estudiante", status_code=404)
    
    return estudiante


@router.get("/", response_model=list[schemas.EstudiantesSalida])
def listar_estudiantes (db: Session = Depends(get_db)):
    estudiante = crud_estudiante.listar_estudiantes(db)

    if not estudiante:
        raise HTTPException (detail="Estudiantes no encontrados", status_code=404)
    
    return estudiante
    


