# 🏥 Système IA de Détection du Cancer du Sein

[![Production](https://img.shields.io/badge/Production-Secure_HTTPS-green.svg)](https://cancer-detection.myftp.org)
[![Python](https://img.shields.io/badge/Language-Python_3.11-blue.svg)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Infrastructure-Docker_Compose-blue.svg)](https://www.docker.com/)

Ce projet présente une solution complète de **Grade Médical** pour l'analyse automatisée de mammographies numériques. Il intègre des recherches avancées en Vision par Ordinateur (Deep Learning) au sein d'une infrastructure logicielle sécurisée.

---

## 🚀 Accès Direct
- **Déploiement Production** : [https://cancer-detection.myftp.org](https://cancer-detection.myftp.org)
- **Identifiants de Test (par mail )** : `mouhamed.ndiaye14@univ-thies.sn`

---

## 🧠 Expertise Machine Learning
Le cœur du système repose sur l'architecture **DenseNet-121**, pré-entraînée sur ImageNet et affinée (Fine-tuning) pour la mammographie.
- **Prétraitement** : Équilibrage d'histogramme, normalisation globale et redimensionnement bicubique.
- **Mapping Dynamique** : Système évitant toute confusion de labels grâce à `classes.json`.
- **Confiance** : Chaque prédiction inclut un score de probabilité Bayesienne pour assister le diagnostic.

---

## 🏗️ Architecture & Composants
Le système est fragmenté en microservices pour une modularité totale.

- **`nginx/`** : Gardien de la sécurité (SSL/TLS v1.3).
- **`frontend/`** : Interface Streamlit optimisée pour l'analyse visuelle.
- **`api-gateway/`** : Chef d'orchestre des requêtes REST.
- **`inference-service/`** : Conteneur hautes performances pour les calculs TensorFlow.
- **`auth-service/`** : Gestionnaire d'identités (Hashage Argon2).
- **`data-service/`** : Gardien de l'historique médical.

---

## 📦 Installation Professionnelle

### Standard (via Docker)
```bash
# Lancement de l'infrastructure complète
docker-compose up -d --build
```

### Pipeline Automatisé (Master script)
```bash
# Automatise de l'entraînement au déploiement VPS
./run_full_pipeline.sh
```

---

## 🛠️ Maintenance & Administration
- **Bascule Local/Prod** : Utilisez `switch_env.sh` (sur le VPS ou localement).
- **Mises à jour IA** : Remplacez simplement le fichier `.h5` dans `inference-service/models/` et relancez le build.
- **Certificats** : Renouvellement automatique assuré par Certbot sur le serveur.

---

## ⚖️ Conformité & Avertissement
Ce logiciel est un **système de recherche**. Bien que performant, il ne doit pas être utilisé comme unique base de diagnostic médical sans supervision humaine qualifiée.

<div align="center">
  
**Département de Informatique**  
© 2026 Projet Master 2

</div>
