# Utilise une image légère de Python comme image de base
FROM python:3.12-slim

# Définit le répertoire de travail dans le conteneur
WORKDIR /app

# Copie les fichiers de dépendances dans le conteneur
COPY requirements.txt .
# Installe les dépendances nécessaires

RUN pip install --no-cache-dir -r requirements.txt

# Copie le reste du code de l'application dans le conteneur
COPY . .

# Lance le serveur uvicorn pour l'application FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
