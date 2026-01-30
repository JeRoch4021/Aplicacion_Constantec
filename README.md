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
Aplicacion_Constantec$ docker compose -f docker-compose-dev.yml up
```

### Como el usuario admin
```shell
Aplicacion_Constantec$ docker exec -it constantec-dev /bin/bash
$ ipython
from models.factories import EstudiantesFactory
from database.connection import SessionLocal
from autenticacion.seguridad import get_password_hash
sesion = SessionLocal()

EstudiantesFactory(no_control="123", nombre="Jeshua", apellidos="Rocha")
EstudiantesFactory(no_control="123", nombre="Jeshua", apellidos="Rocha", contrasena=get_password_hash("passworddiferente"))
AdminFactory(username="admin")
```

## Los contenedores internamente ya tienen instalado ruff, mypy y pre-commit

### Pero si quieres utilizarlo en tu host (computadora), entonces descarga las siguientes herraminetas:

#### Para formater
``` shell
pip install ruff
```
#### Para linter
``` shell
pip install mypy
```
#### Para pre-commit
``` shell
pip install pre-commit
```
#### Para activar el framework pre-commit, el cual al configurar los ganchos (hooks) de Git, se ejecutaran automáticamente.
``` shell
pre-commit install
```

## Comandos extra

#### 1. Corrige y organiza imports automáticamente 
``` shell
ruff check . --fix
``` 

#### 2. Da formato estético al código 
``` shell
ruff format .
``` 

#### 3. Verifica que no existan errores de tipos en ninguna tabla 
``` shell
mypy . > errores.txt
``` 

#### Para generar una lista detallada de todos los paquetes de Python instalados en el entorno actual.
``` shell
pip freeze > requirements_dev.txt
```

#### Para preparar la aplicación web en un entorno de producción.
``` shell
npm run build
```

#### Para mover el disco a una carpeta lista para ser empaquetada en el contenedor de docker.
``` shell
mv dist ../api-constantec/web-app
```