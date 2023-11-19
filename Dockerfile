# Usa una imagen base de Python 3.11.5
FROM python:3.11.5

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos de requerimientos (requirements.txt) al directorio de trabajo
COPY requirements.txt .

# Instala las dependencias utilizando pip
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto de tu aplicación al directorio de trabajo
COPY . .

# Especifica el comando predeterminado a ejecutar cuando se inicia el contenedor
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
