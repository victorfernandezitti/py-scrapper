# 1. Usar una imagen base de Python
FROM python:3.10-slim

# Etiqueta para identificar al autor
LABEL maintainer="tu-nombre@ejemplo.com"

# 2. Instalar dependencias del sistema y Google Chrome (MÉTODO MODERNO Y SEGURO)
RUN apt-get update && apt-get install -y \
    ca-certificates \
    gnupg \
    wget \
    --no-install-recommends \
    # Crear el directorio para las claves si no existe
    && mkdir -p /etc/apt/keyrings \
    # Descargar la clave de Google, convertirla al formato correcto y guardarla
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /etc/apt/keyrings/google-chrome.gpg \
    # Añadir el repositorio de Chrome, especificando dónde está la clave para la firma
    && echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
    # Actualizar la lista de paquetes e instalar Chrome
    && apt-get update \
    && apt-get install -y google-chrome-stable --no-install-recommends \
    # Limpiar todo para reducir el tamaño de la imagen
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 3. Configurar el entorno de la aplicación
WORKDIR /app

# 4. Instalar las dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiar el script de la aplicación
COPY index.py .

# 6. Comando para ejecutar la aplicación
CMD ["python", "index.py"]
