from sqlalchemy.orm import Session
from Database.database import SessionLocal
from Models import models
#from Models.security import cifrar_contrasena
import bcrypt


def cifrar_contrasena(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def es_bcrypt_hash(contrasena: str) -> bool:
    # Un hash bcrypt válido empieza con $2b$ o $2a$ y tiene longitud 60
    return contrasena.startswith("$2b$") or contrasena.startswith("$2a$") and len(contrasena) == 60

def actualizar_contrasenas():
    db: Session = SessionLocal()
    estudiantes = db.query(models.Estudiantes).all()
    actualizados = 0

    for estudiante in estudiantes:
        if not es_bcrypt_hash(estudiante.Contrasena):
            hash_nuevo = cifrar_contrasena(estudiante.Contrasena)
            estudiante.Contrasena = hash_nuevo
            actualizados += 1

    db.commit()
    db.close()
    print(f"Contraseñas actualizadas: {actualizados}")

if __name__ == "__main__":
    actualizar_contrasenas()