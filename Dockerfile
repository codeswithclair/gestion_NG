# Dockerfile para el backend Flask de Noreste Grill (gestion_NG).
FROM python:3.12-slim

WORKDIR /app

# Instalar dependencias primero para aprovechar la cache de capas de Docker.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del proyecto (backend, templates, static, database, etc).
COPY . .

EXPOSE 5000

# Ejecuta la app tal como se documenta en README/ONBOARDING.
# waitress-serve (producción) se configura en GN-16.
CMD ["python", "-m", "backend.test_app"]
