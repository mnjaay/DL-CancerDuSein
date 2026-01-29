#!/bin/bash

# 🚀 Script de Pipeline Complet : Preprocessing -> Training -> Deployment
# Ce script automatise tout le flux de travail.

set -e # Arrête le script en cas d'erreur

# Couleurs pour la lisibilité
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}================================================${NC}"
echo -e "${BLUE}🏥 Cancer Detection System - Pipeline Complet${NC}"
echo -e "${BLUE}================================================${NC}"

# 1. Vérification de l'environnement virtuel
echo -e "\n${YELLOW}[1/4] Vérification de l'environnement...${NC}"
if [ ! -d "ml/venv" ]; then
    echo -e "${YELLOW}⚠️ Environnement virtuel non trouvé. Lancment du setup...${NC}"
    ./setup_ml.sh
fi

source ml/venv/bin/activate
echo -e "${GREEN}✅ Environnement Python activé.${NC}"

# 2. Préparation des données (Cleaning + Splitting)
echo -e "\n${YELLOW}[2/4] Vérification des données...${NC}"

if [ -d "ml/data/raw" ] && [ "$(ls -A ml/data/raw)" ]; then
    echo -e "${BLUE}Images trouvées dans ml/data/raw. Lancement de la préparation (splitting)...${NC}"
    python ml/preprocessing.py prepare --input ml/data/raw --output ml/data --size 128
    echo -e "${GREEN}✅ Données préparées et réparties dans ml/data/.${NC}"
elif [ -d "ml/data/train" ] && [ "$(ls -A ml/data/train)" ]; then
    echo -e "${GREEN}✅ Dossier d'entraînement déjà présent. Passage à l'entraînement.${NC}"
else
    echo -e "${RED}❌ Erreur : Pas de données trouvées dans ml/data/raw ni dans ml/data/train.${NC}"
    echo -e "Veuillez placer vos images dans ml/data/raw (pour splitting) ou directement dans ml/data/train/Positive et ml/data/train/Negative."
    exit 1
fi

# 3. Entraînement du modèle
echo -e "\n${YELLOW}[3/4] Entraînement du modèle CNN...${NC}"
python ml/train.py --config ml/config.yaml
echo -e "${GREEN}✅ Entraînement terminé. Nouveau modèle généré.${NC}"

# 4. Déploiement Docker
echo -e "\n${YELLOW}[4/4] Déploiement des conteneurs Docker...${NC}"
echo -e "${BLUE}Reconstruction de l'image d'inférence...${NC}"
docker compose build inference-service

# Optionnel : Push vers Docker Hub pour le VPS
read -p "Voulez-vous pousser l'image sur Docker Hub pour le VPS ? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    IMAGE_NAME="mnjaay312/cancer-detection-inference:latest"
    echo -e "${BLUE}📤 Push vers Docker Hub : $IMAGE_NAME...${NC}"
    docker push $IMAGE_NAME
    echo -e "${GREEN}✅ Image poussée avec succès.${NC}"
fi

echo -e "\n${BLUE}Lancement des services locaux...${NC}"
docker compose up -d

echo -e "\n${GREEN}================================================${NC}"
echo -e "${GREEN}✨ PIPELINE TERMINÉ AVEC SUCCÈS !${NC}"
echo -e "${GREEN}================================================${NC}"
echo -e "Votre application est à jour et disponible sur : ${BLUE}http://localhost:8501${NC}"

deactivate
