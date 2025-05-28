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