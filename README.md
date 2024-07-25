
# Gestión de Seguridad en Infraestructura

## Descripción General del Proyecto

Este proyecto es una API REST desarrollada con Django REST Framework para gestionar la seguridad de los sistemas desplegados en la infraestructura Cloud mediante el cruce de información con los CVEs del NIST. La aplicación permite:

1. Obtener un listado de todas las vulnerabilidades del NIST.
2. Indicar qué vulnerabilidades ya se han corregido en la infraestructura.
3. Obtener un listado de vulnerabilidades excluyendo las que ya se han corregido.
4. Obtener información resumida de vulnerabilidades por severidad.

## Requisitos del Sistema

- Python 3.9+
- Django 4.2.14
- Django REST Framework
- PostgreSQL
- Docker & Docker Compose

## Instalación y Configuración

### Clonar el Repositorio

```bash
git clone https://github.com/jairoCO10/security_management.git
cd security_management
```

### Configuración del Entorno

Crear y activar un entorno virtual (opcional pero recomendado):

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

Instalar las dependencias:

```bash
pip install -r requirements.txt
```
### Archivo .env

```Properties

# POSTGRES
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
PGADMIN_DEFAULT_EMAIL=admin@example.com
PGADMIN_DEFAULT_PASSWORD=
PORTPG=5050:80
HOST=

SECRET_KEY =''


ENVIROMEN= DEBUG

DEBUG=False

DEPLOY = DEV
```

### Configuración de la Base de Datos

Crear y configurar la base de datos PostgreSQL. Asegúrate de que tu configuración de base de datos en `settings.py` se vea algo así:

```python
DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("POSTGRES_DB"), 
            "USER": os.getenv("POSTGRES_USER"), 
            "PASSWORD": os.getenv("POSTGRES_PASSWORD"), 
            "HOST": "postgres", # O la IP o nombre del contenedor de la base de datos
            "PORT": "5432", 
        }
    }
```

### Migraciones de la Base de Datos

```bash
python manage.py migrate
```
### Configuracion de archivo  `run.py`
 run.py es un script de python el cual es el encargado de cargar todas las vulnerabilidades a la db

![Diagrama de la Solución](img/code.png)


### Cargar Datos Iniciales

```bash
python manage.py shell < run.py
```

## Guía de Uso

### Iniciar la Aplicación

```bash
python manage.py runserver
```

### Endpoints de la API

1. **Listar Vulnerabilidades**

   - **URL**: `/api/vulnerabilities/`
   - **Método**: `GET`
   - **Descripción**: Devuelve el listado total de las vulnerabilidades.
   - **Ejemplo de Solicitud**:
     ```bash
     curl -X GET http://localhost:8010/api/vulnerabilities/
     ```

2. **Registrar Vulnerabilidades Corregidas**

   - **URL**: `/api/fixed-vulnerabilities/`
   - **Método**: `POST`
   - **Descripción**: Recibe las vulnerabilidades corregidas.
   - **Ejemplo de Solicitud**:
     ```bash
     curl -X POST http://localhost:8010/api/fixeds/ -d '{"cve_id": "CVE-2000-0564"}'
     ```

3. **Listar Vulnerabilidades Excluyendo las Corregidas**

   - **URL**: `/api/vulnerabilities/excluding-fixed/`
   - **Método**: `GET`
   - **Descripción**: Devuelve el listado de vulnerabilidades excluyendo las corregidas.
   - **Ejemplo de Solicitud**:
     ```bash
     curl -X GET http://localhost:8010/api/vulnerabilities/excluding-fixed/
     ```

4. **Resumen de Vulnerabilidades por Severidad**

   - **URL**: `/api/vulnerabilities/summary/`
   - **Método**: `GET`
   - **Descripción**: Devuelve un resumen de vulnerabilidades por severidad.
   - **Ejemplo de Solicitud**:
     ```bash
     curl -X GET http://localhost:8010/api/vulnerabilities/summary/
     ```

## Testing

### Ejecutar Pruebas

Las pruebas se han implementado utilizando `pytest`. Para ejecutarlas, usa el siguiente comando:

```bash
pytest --html=report.html --self-contained-html
```
![Diagrama de la Solución](img/report.png)

### Test Coverage

```bash
pytest --html=report.html --self-contained-html
```
![Diagrama de la Solución](img/coverage.png)



## Dockerización

### Construir y Ejecutar el Contenedor

Asegúrate de tener Docker y Docker Compose instalados. Luego, sigue estos pasos:
   ```bash
   docker --version && docker-compose --version
   ```


1. Ejecutar los contenedores:

   ```bash
   docker-compose up --build -d
   ```

2. :

   ```bash
   docker logs <CONTAINER ID>
   ```

### Archivo `docker-compose.yml`

```yaml
version: "3.9"

services:
  postgres:
    image: postgres:latest
    container_name: postgres
    environment:
      POSTGRES_DB: ${POSTGRES_DB}
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    ports:
      - "5432:5432"
    volumes:
      - ./postgres_data:/var/lib/postgresql

  pgadmin:
    image: dpage/pgadmin4:latest
    environment:
      PGADMIN_DEFAULT_EMAIL: ${PGADMIN_DEFAULT_EMAIL}
      PGADMIN_DEFAULT_PASSWORD: ${PGADMIN_DEFAULT_PASSWORD}
      PGADMIN_CONFIG_ENHANCED_COOKIE_PROTECTION: "True"
      PGADMIN_CONFIG_CHECK_FOR_NEWER_VERSIONS: "False"
      PGADMIN_CONFIG_CONSOLE_LOG_LEVEL: "10"
    ports:
      - ${PORTPG}
    depends_on:
      - postgres

  security_management:
    build: .
    ports:
      - "8010:8000"
    depends_on:
      - postgres

```

## Estructura del Proyecto

La aplicación sigue la arquitectura hexagonal y los principios SOLID. La estructura del proyecto es la siguiente:

```
/security_management
│
├── manage.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env
│
├── /security_management
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   ├── asgi.py
│   │
├── /vulneravility
│   ├── __init__.py
│   ├── urls.py
│   ├── views.py
│   ├── models.py
│   ├── admin.py
│   ├── apps.py
│   └── tests.py
│   ├──/entities
│   │   └── VulnerabilityEntities.py
│   ├──/interface_adapters
│   │   ├──/controller
│   │   │   └── VulnerabilityControl.py
│   │   ├──/dependencies
│   │   │   └── openapidoc.py
│   │   ├──/gateways
│   │   │   └── VulnerabilityGateways.py
│   ├──/repository
│   │   └── VulnerabilityRepository.py
│   ├──/serializers
│   │   └── serializers.py
│   ├──/usecases
│   │   └── VulnerabilityCases.py
├── /fixedVulnerability
│   ├── __init__.py
│   ├── urls.py
│   ├── views.py
│   ├── models.py
│   ├── admin.py
│   ├── apps.py
│   └── tests.py
│   ├──/entities
│   │   └── FixedEntities.py
│   ├──/interface_adapters
│   │   ├──/controller
│   │   │   └── FixedControl.py
│   │   ├──/dependencies
│   │   │   └── openapidoc.py
│   │   ├──/gateways
│   │   │   └── FixedGateways.py
│   ├──/repository
│   │   └── FixedRepository.py
│   ├──/serializers
│   │   └── serializers.py
│   ├──/usecases
│   │   └── FixedCases.py
```

## Autenticación y Autorización

### Implementación

La autenticación y autorización se puede implementar utilizando JWT (JSON Web Tokens) con Django REST Framework. Para detalles sobre cómo configurar esto, consulta la [documentación de Django REST Framework Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/).

### Ejemplo de Configuración

1. Instalar `djangorestframework-simplejwt`:

   ```bash
   pip install djangorestframework-simplejwt
   ```

2. Añadir la configuración en `settings.py`:

   ```python
   REST_FRAMEWORK = {
       'DEFAULT_AUTHENTICATION_CLASSES': (
           'rest_framework_simplejwt.authentication.JWTAuthentication',
       ),
   }

   SIMPLE_JWT = {
       'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
       'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
   }
   ```
3.  Implementación de los endpoints

  ```python

  from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView,)

  urlpatterns = [
      path('admin/', admin.site.urls),
      path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
      path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
      ...
  ]
   ```
4. Prueba de servicio
```bash
curl --location 'http://localhost:8010/api/token/' \
--header 'Content-Type: application/json' \
--data '{
    "username": "user",
    "password": "test"
}'
```
```json
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcyMTk2NDAyNSwiaWF0IjoxNzIxODc3NjI1LCJqdGkiOiI5OGExN2I3NWFkNjM0YzM0YWU5NDc1ZTkzNDk5YjhmMSIsInVzZXJfaWQiOjF9.fuY9mZ9hlsAO-MA2vQ0qB6ZFqUTVY4b37jiCgx8GSVU",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzIxODc3OTI1LCJpYXQiOjE3MjE4Nzc2MjUsImp0aSI6IjllZTgwZjYwNzVkZjRiZDI4YTBlZDU2YTdhMTNiMDE2IiwidXNlcl9pZCI6MX0.xGQMqf61XtdZ-JA_ljw3hhZlDKhCN7FjO6WcHSqVSuM"
}
```
5. Prueba de un endpont con el token
```bash
curl --location 'http://localhost:8010/api/vulnerabilities/excluding-fixed/' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzIxODc3OTI1LCJpYXQiOjE3MjE4Nzc2MjUsImp0aSI6IjllZTgwZjYwNzVkZjRiZDI4YTBlZDU2YTdhMTNiMDE2IiwidXNlcl9pZCI6MX0.xGQMqf61XtdZ-JA_ljw3hhZlDKhCN7FjO6WcHSqVSuM'
```
### Nota:
Si el token no se proporciona la respuesta sera la siguiente
```json
{
    "detail": "Authentication credentials were not provided."
}
```
## Despliegue

### Desplegar en Producción

Para desplegar la aplicación en un entorno de producción, sigue estos pasos:

1. Configurar un servidor con Docker.
2. Configurar la base de datos PostgreSQL en el servidor.
3. Construir y ejecutar el contenedor Docker en el servidor.


## Logs y Auditoría

### Implementación

Los logs y auditoría se pueden implementar utilizando el módulo `logging` de Python.

### Ejemplo de Configuración

```python
import logging
from logging.handlers import TimedRotatingFileHandler

# Configuración del logger
log_formatter = logging.Formatter('%(asctime)s [%(levelname)s] - %(message)s')
log_handler = TimedRotatingFileHandler(
    filename='logs/vulnerability/vulnerability.log',
    when='D',
    interval=1,
)
log_handler.setFormatter(log_formatter)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(log_handler)

@api_view(['GET'])
def get_all(request):
    control = ControlVulnerability()
    try:
        vulnerabilities = control.get_all_vulnerability()
        serializer = VulnerabilityDataClassSerializer(vulnerabilities, many=True)
        logger.info("Solicitud a la ruta /vulnerabilities.\n")
        return Response(serializer.data)
    except Http404:
        logger.error(notfound_message)
        raise NotFound(notfound_message)
        
```
# Documentacion de endpoint
para esta api se creo por medio de django-yrf una documentacion la cual puede ser consultada en el siguiente enlace, esta contiene la estrutura que se usa en los distintos endpoints
[enlace](http://localhost:8010/redoc)


## Contribución

Para contribuir a este proyecto, sigue estos pasos:

1. Haz un fork del repositorio.
2. Crea una rama (`git checkout -b feature/NombreDeTuRama`).
3. Realiza tus cambios y commitea (`git commit -am 'Añade alguna funcionalidad'`).
4. Sube tus cambios a tu fork (`git push origin feature/NombreDeTuRama`).
5. Crea un nuevo Pull Request.

## Licencia

Este proyecto está licenciado bajo los términos de la licencia MIT. Consulta el archivo `LICENSE` para más información.
---