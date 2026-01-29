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

# 2. Nettoyage et Vérification des données
echo -e "\n${YELLOW}[2/4] Nettoyage et Vérification...${NC}"

if [ -d "ml/data/train" ] && [ -d "ml/data/val" ] && [ -d "ml/data/test" ]; then
    echo -e "${GREEN}✅ Répertoires de données trouvés.${NC}"
    # Lancement du script de nettoyage/vérification comme demandé
    python ml/preprocessing.py check --data_dir ml/data
    echo -e "${GREEN}✅ Nettoyage et vérification terminés.${NC}"
else
    echo -e "${RED}❌ Erreur : Répertoires de données (train, val, test) manquants.${NC}"
    echo -e "Veuillez vous assurer que vos dossiers sont bien dans ml/data/."
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

    # 5. Déploiement à distance (VPS)
    echo -e "\n${YELLOW}[5/5] Déploiement automatique sur le VPS...${NC}"
    read -p "Voulez-vous mettre à jour le VPS (root@srv1306353) ? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        VPS_HOST="srv1306353"
        VPS_USER="root"
        VPS_PATH="~/DL-CancerDuSein"
        
        echo -e "${BLUE}⚡ Connexion à $VPS_HOST et mise à jour...${NC}"
        ssh ${VPS_USER}@${VPS_HOST} "cd ${VPS_PATH} && docker compose pull inference-service && docker compose up -d inference-service"
        
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}✅ VPS mis à jour avec succès !${NC}"
        else
            echo -e "${RED}❌ Erreur lors de la mise à jour du VPS. Vérifiez votre connexion SSH.${NC}"
        fi
    fi
fi

echo -e "\n${BLUE}Lancement des services locaux...${NC}"
docker compose up -d

echo -e "\n${GREEN}================================================${NC}"
echo -e "${GREEN}✨ PIPELINE TERMINÉ AVEC SUCCÈS !${NC}"
echo -e "${GREEN}================================================${NC}"
echo -e "Votre application est à jour et disponible sur : ${BLUE}http://localhost${NC}"

deactivate
