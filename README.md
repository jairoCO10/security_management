# Proyecto de Gestión de Vulnerabilidades

Este proyecto implementa un sistema para la gestión de vulnerabilidades, aplicando principios de Clean Code, SOLID y arquitectura hexagonal. La aplicación está desarrollada con Django y se ejecuta en un entorno Docker que incluye pgAdmin y PostgreSQL.

## Requisitos

Asegúrate de tener Docker y Docker Compose instalados en tu máquina. Puedes verificarlo con los siguientes comandos:

```sh
docker --version && docker-compose --version
```


## Estructura del Proyecto
* Django: El framework principal para construir la API.
* pgAdmin: Herramienta de administración para PostgreSQL.
* PostgreSQL: Base de datos utilizada para almacenar la información.

# Configuración


1. Variables de Entorno
```sh
POSTGRES_DB=test
POSTGRES_USER=root
POSTGRES_PASSWORD=test
PGADMIN_DEFAULT_EMAIL=admin@example.com
PGADMIN_DEFAULT_PASSWORD=test
PORTPG=5050:80
```
Crea un archivo .env en la raíz del proyecto con las siguientes variables:


## Ejecución
1. Para iniciar la aplicación, sigue estos pasos:

    * Construir y levantar los contenedores

    * Ejecuta el siguiente comando en la raíz del proyecto:

    ```shell
    docker-compose up --build -d
    ```
    Esto construirá los contenedores y los levantará. La aplicación Django estará 
    disponible en http://localhost:8010.

2. Aplicar Migraciones

    Una vez que los contenedores estén en ejecución, aplica las migraciones de Django:

    ```shell
    docker-compose exec security_management python manage.py migrate
    ```
3. Acceder a pgAdmin

    Abre tu navegador y accede a pgAdmin en http://localhost:5050. Usa las credenciales 
    definidas en el archivo .env para iniciar sesión.



# Implementación

## Clean Code

El proyecto sigue los principios de Clean Code para asegurar un código claro y mantenible.

## Principios SOLID

* S: Responsabilidad Única
* O: Abierto/Cerrado
* L: Sustitución de Liskov
* I: Segregación de Interfaces
* D: inyección de Dependencias

## Arquitectura Hexagonal
La aplicación está diseñada siguiendo el patrón de arquitectura hexagonal, lo que facilita la separación de las distintas capas y permite una mejor gestión de las dependencias y la integración de componentes.


# Uso de la API
Crear una Vulnerabilidad

Endpoint: POST /api/vulnerabilities/
Request Body: Debe incluir los detalles de la vulnerabilidad.
Obtener Todas las Vulnerabilidades

Endpoint: GET /api/vulnerabilities/

## Notas Adicionales
Si realizas cambios en el código, asegúrate de reconstruir los contenedores con:
 ```shell
 docker-compose up --build

 docker-compose exec security_management python manage.py migrate

 ```

# Test en html
 ```shell
pytest --html=report.html --self-contained-html   

 ```
![Texto alternativo](/img/report.png)


 
# Test Coverage
 ```shell
pytest --cov=security_management --cov-report=html  
 ```
 ![Texto alternativo](/img/coverage.png)


# Insertar los registros a al db
 ```shell
python manage.py shell < run.py
 ```
 Este escript es el encargado de carga la db con toda la informacion (https://nvd.nist.gov/developers/vulnerabilities).

 ![Texto alternativo](/img/django.png)



# Documentacion 

[documentacion de la endpoint](http://localhost:8000/redoc/)
 