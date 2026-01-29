#!/bin/bash

# Script pour construire l'image d'inférence localement et la pousser sur Docker Hub
# Cela permet de contourner les limites de GitHub LFS

# Charger les variables (ou demander si absentes)
DEFAULT_DOCKER_USER="mnjaay312"
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
if ! docker build -t $IMAGE_NAME ./inference-service; then
    echo "❌ Erreur lors du build Docker. Vérifiez que Docker Desktop est lancé sur votre Mac."
    exit 1
fi

echo "📤 Push vers Docker Hub..."
if ! docker push $IMAGE_NAME; then
    echo "❌ Erreur lors du push Docker sur Docker Hub."
    exit 1
fi

echo "✅ Terminé ! L'image est disponible sur Docker Hub."
echo "Vous pouvez maintenant mettre à jour votre VPS."
