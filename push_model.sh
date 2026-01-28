#!/bin/bash

# Script pour construire l'image d'inférence localement et la pousser sur Docker Hub
# Cela permet de contourner les limites de GitHub LFS

# Charger les variables (ou demander si absentes)
DEFAULT_DOCKER_USER="mnjaay"
read -p "Entrez votre nom d'utilisateur Docker Hub [$DEFAULT_DOCKER_USER]: " DOCKER_USER
DOCKER_USER=${DOCKER_USER:-$DEFAULT_DOCKER_USER}

IMAGE_NAME="$DOCKER_USER/cancer-detection-inference:latest"

echo "🚀 Début de la préparation de l'image..."

# Vérifier si le modèle existe localement
if [ ! -f "inference-service/models/model.h5" ]; then
    echo "❌ Erreur : inference-service/models/model.h5 introuvable !"
    exit 1
fi

echo "📦 Construction de l'image Docker : $IMAGE_NAME"
docker build -t $IMAGE_NAME ./inference-service

echo "📤 Push vers Docker Hub..."
docker push $IMAGE_NAME

echo "✅ Terminé ! L'image est disponible sur Docker Hub."
echo "Vous pouvez maintenant mettre à jour votre VPS."
