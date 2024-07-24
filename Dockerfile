# Utiliza una imagen base de Python
FROM python:3.9-slim

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia el archivo requirements.txt y lo instala
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Copia el resto de la aplicación
COPY . /app/

# Expone el puerto 8000 para el servidor Django
EXPOSE 8000

# Comando para ejecutar el servidor Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

