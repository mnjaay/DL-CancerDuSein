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
echo -e "\n${YELLOW}[2/4] Nettoyage et préparation des données (Train/Val/Test)...${NC}"
if [ ! -d "ml/data/raw" ] || [ -z "$(ls -A ml/data/raw)" ]; then
    echo -e "${RED}❌ Erreur : Pas d'images trouvées dans ml/data/raw.${NC}"
    echo -e "Veuillez copier vos images dans ml/data/raw/Positive et ml/data/raw/Negative avant de continuer."
    exit 1
fi

python ml/preprocessing.py prepare --input ml/data/raw --output ml/data --size 128
echo -e "${GREEN}✅ Données préparées et réparties dans ml/data/.${NC}"

# 3. Entraînement du modèle
echo -e "\n${YELLOW}[3/4] Entraînement du modèle CNN...${NC}"
python ml/train.py --config ml/config.yaml
echo -e "${GREEN}✅ Entraînement terminé. Nouveau modèle généré.${NC}"

# 4. Déploiement Docker
echo -e "\n${YELLOW}[4/4] Déploiement des conteneurs Docker...${NC}"
echo -e "${BLUE}Reconstruction de l'image d'inférence avec le nouveau modèle...${NC}"
docker compose up -d --build inference-service

echo -e "\n${BLUE}Redémarrage des autres services si nécessaire...${NC}"
docker compose up -d

echo -e "\n${GREEN}================================================${NC}"
echo -e "${GREEN}✨ PIPELINE TERMINÉ AVEC SUCCÈS !${NC}"
echo -e "${GREEN}================================================${NC}"
echo -e "Votre application est à jour et disponible sur : ${BLUE}http://localhost:8501${NC}"

deactivate
