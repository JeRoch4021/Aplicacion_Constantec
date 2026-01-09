# Aplicacion_Constantec
Repositorio para el desarrollo de la aplicación que gestionará las constancias

### Como crear una imagen de desarrollo de constatec
```shell
Aplicacion_Constantec$ docker build -f ./dockerfiles/Dockerfile.dev -t jeshuarocha/constantec_dev:{VERSION!} -t jeshuarocha/constantec_dev:latest .
```
Nota: modificar la version del docker image

### Como publicar una nueva imagen a docker hub
```shell
Aplicacion_Constantec$ docker push jeshuarocha/constantec:latest
Aplicacion_Constantec$ docker push jeshuarocha/constantec:{VERSION!}
```
Nota: modificar la version del docker image

### Como crear containers para modo desarrollo con docker compose
```shell
Aplicacion_Constantec$ docker compose -f docker-compose-dev.yml up --force-recreate
```

### Como el usuario admin
```shell
Aplicacion_Constantec$ docker exec -it constantec-dev /bin/bash
$ ipython
from models.factories import EstudiantesFactory
from database.connection import SessionLocal
from autenticacion.seguridad import get_password_hash
sesion = SessionLocal()

EstudiantesFactory(no_control="22240302", nombre="Jeshua", apellidos="Rocha Sainez")
EstudiantesFactory(no_control="22240302", nombre="Jeshua", apellidos="Rocha Sainez", contrasena=get_password_hash("passworddiferente"))
```

### Como iniciar el servidor desde el container de fastapi
```shell
Aplicacion_Constantec$ docker exec -it constantec-dev /bin/bash
/app $ uvicorn main:app --host 0.0.0.0 --port 8000 --reload --log-level debug
```