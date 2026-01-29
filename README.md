# 🏥 Système de Détection du Cancer du Sein par IA

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.15+-orange.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)
![SSL](https://img.shields.io/badge/SSL-HTTPS-green.svg)
![Docker](https://img.shields.io/badge/Docker-Microservices-blue.svg)

**Solution IA sécurisée pour l'analyse mammographique | HTTPS : [cancer-detection.myftp.org](https://cancer-detection.myftp.org)**

</div>

---

## 🌟 Vue d'ensemble
Ce projet implémente un système de détection du cancer du sein utilisant le Deep Learning (**DenseNet121**). L'architecture est basée sur des **microservices** pour garantir une scalabilité et une sécurité de niveau hospitalier.

### 🛡️ Caractéristiques Principales
- 🧠 **DenseNet121** : Précision accrue via Transfer Learning.
- 🔒 **HTTPS Global** : Sécurisation via Let's Encrypt et Nginx.
- 🚧 **API Gateway** : Orchestration centralisée et masquage de l'infrastructure interne.
- 📈 **Dashboard Premium** : Interface Streamlit avec historique et statistiques en temps réel.
- 🚀 **Pipeline "One-Click"** : Entraînement et déploiement VPS automatisés.

---

## 🏗️ Architecture Technique
Le système s'articule autour d'un **Reverse Proxy Nginx** qui sert de barrière de sécurité et de point d'entrée unique.

| Composant | Technologie | Rôle |
| :--- | :--- | :--- |
| **Frontend** | Streamlit | Interface utilisateur Premium |
| **API Gateway** | FastAPI | Routage et agrégation inter-services |
| **Auth Service** | FastAPI + JWT | Sécurité et accès (Login uniquement) |
| **Inference** | TensorFlow | Moteur de prédiction IA |
| **Data Service** | FastAPI + SQL | Persistance des analyses |
| **Database** | PostgreSQL | Stockage SQL robuste |

---

## 🚀 Démarrage

### 🚀 Production (VPS)
Le site est déployé et sécurisé sur : `https://cancer-detection.myftp.org`

### 💻 Local (Mac/PC)
1. Clonez le projet.
2. Lancez le pipeline :
   ```bash
   chmod +x run_full_pipeline.sh
   ./run_full_pipeline.sh
   ```
3. Accédez à `http://localhost`.

---

## 📁 Structure du Projet
```text
.
├── 📂 nginx/             # Configuration Reverse Proxy & SSL
├── 📂 api-gateway/       # Passerelle unique (FastAPI)
├── 📂 auth-service/      # Gestion identité (JWT)
├── 📂 inference-service/ # Moteur IA (DenseNet121)
├── 📂 data-service/      # CRUD & Statistiques
├── 📂 frontend/          # Streamlit v2 (Premium)
├── 📂 ml/                # Pipeline d'entraînement IA
└── docker-compose.yml    # Orchestration générale
```

---

## ⚠️ Avertissement Médical
Ce système est un **outil d'aide à la décision** à des fins de recherche. Il ne remplace en aucun cas un diagnostic médical. Toute analyse doit être validée par un professionnel de santé qualifié.

---

<div align="center">
Made with ❤️ | © 2026 Cancer Detection Project
</div>
