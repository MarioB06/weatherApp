FROM python:3.12-slim

# Arbeitsverzeichnis im Container
WORKDIR /app

# keine pyc-Dateien / stdout sofort
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Dependencies installieren
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Code ins Image
COPY . .

# Port freigeben
EXPOSE 8000

# Startkommando (kann docker-compose überschreiben)
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
