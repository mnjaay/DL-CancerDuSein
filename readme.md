# 🏥 Système de Détection du Cancer du Sein par IA

<div align="center">

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-orange.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**Système intelligent de détection du cancer du sein utilisant des réseaux de neurones convolutifs (CNN) avec architecture microservices**

[Démarrage Rapide](#-démarrage-rapide) • [Documentation](#-documentation) • [Architecture](#-architecture) • [API](#-api) • [Déploiement](#-déploiement)

</div>

---

## 📋 Table des Matières

- [Vue d'ensemble](#-vue-densemble)
- [Caractéristiques](#-caractéristiques)
- [Architecture](#-architecture)
- [Prérequis](#-prérequis)
- [Installation](#-installation)
- [Démarrage Rapide](#-démarrage-rapide)
- [Utilisation](#-utilisation)
- [Structure du Projet](#-structure-du-projet)
- [API Documentation](#-api)
- [Technologies Utilisées](#-technologies-utilisées)
- [Déploiement](#-déploiement)
- [Troubleshooting](#-troubleshooting)
- [Contribution](#-contribution)
- [License](#-license)

---

## 🎯 Vue d'ensemble

Ce projet implémente un **système complet de détection du cancer du sein** utilisant l'intelligence artificielle (Deep Learning) pour analyser des images mammographiques. Le système est construit avec une **architecture microservices moderne** et offre une interface utilisateur intuitive pour les professionnels de la santé.

### 🌟 Points Clés

- 🧠 **Modèle CNN** entraîné pour détecter le cancer du sein
- 🏗️ **Architecture microservices** scalable et maintenable
- 🔐 **Authentification JWT** sécurisée
- 📊 **Visualisations interactives** des résultats et statistiques
- 🐳 **Containerisation Docker** pour déploiement facile
- 🌐 **Exposition publique** via ngrok pour démos

---

## ✨ Caractéristiques

### Fonctionnalités Principales

- ✅ **Upload et Analyse d'Images**
  - Support des formats JPG, JPEG, PNG
  - Analyse en temps réel avec CNN
  - Score de confiance pour chaque prédiction

- 📊 **Tableau de Bord Complet**
  - Historique des prédictions
  - Statistiques globales avec graphiques interactifs
  - Export des données en CSV
  - Filtres et recherche

- 🔒 **Sécurité**
  - Authentification utilisateur (JWT)
  - Gestion des sessions
  - CORS configuré
  - Variables d'environnement sécurisées

- 🎨 **Interface Moderne**
  - Design responsive
  - Visualisations Plotly interactives
  - Navigation par onglets
  - Indicateurs visuels clairs

---

## 🏗️ Architecture

### Schéma de l'Architecture

```mermaid
graph TB
    subgraph "Client Layer"
        A[🌐 Frontend Streamlit<br/>Port 8501]
    end
    
    subgraph "API Gateway Layer"
        B[🚪 API Gateway<br/>Port 8004]
    end
    
    subgraph "Services Layer"
        C[🔐 Auth Service<br/>Port 8000]
        D[🧠 Inference Service<br/>Port 8001]
        E[💾 Data Service<br/>Port 8002]
    end
    
    subgraph "Data Layer"
        F[(🗄️ PostgreSQL<br/>Port 5432)]
    end
    
    A -->|HTTPS Requests| B
    B -->|Auth| C
    B -->|Predictions| D
    B -->|CRUD| E
    C -->|Users DB| F
    E -->|Predictions DB| F
    D -.->|Save Results| E
    
    style A fill:#e1f5ff
    style B fill:#fff4e1
    style C fill:#ffe1f5
    style D fill:#e1ffe1
    style E fill:#f5e1ff
    style F fill:#ffe1e1
```

### Services

| Service | Rôle | Port | Technologies |
|---------|------|------|--------------|
| **Frontend** | Interface utilisateur | 8501 | Streamlit, Plotly, Pandas |
| **API Gateway** | Point d'entrée unique, routage | 8004 | FastAPI, HTTPX |
| **Auth Service** | Authentification JWT | 8000 | FastAPI, SQLAlchemy, Jose |
| **Inference Service** | Prédictions CNN | 8001 | FastAPI, TensorFlow, Pillow |
| **Data Service** | CRUD prédictions | 8002 | FastAPI, SQLAlchemy |
| **PostgreSQL** | Base de données | 5432 | PostgreSQL 15 |

---

## 📦 Prérequis

### Logiciels Requis

- **Docker** ≥ 20.10
- **Docker Compose** ≥ 2.0
- **Python** ≥ 3.9 (pour développement local)
- **Git**

### Optionnel

- **ngrok** (pour exposition publique)
- **Postman** (pour tester l'API)

### Vérification

```bash
# Vérifier Docker
docker --version
docker-compose --version

# Vérifier Python (optionnel)
python --version
```

---

## 🚀 Installation

### 1. Cloner le Repository

```bash
git clone https://github.com/mnjaay/DL-CancerDuSein.git
cd DL-CancerDuSein
```

### 2. Configuration des Variables d'Environnement

Le projet utilise des fichiers `.env` dans chaque service. Voici les configurations par défaut :

#### `api-gateway/.env`
```env
AUTH_SERVICE_URL=http://auth-service:8000
INFERENCE_SERVICE_URL=http://inference-service:8001
DATA_SERVICE_URL=http://data-service:8002
```

#### `auth-service/.env`
```env
DATABASE_URL=postgresql://user:password@postgres:5432/auth_db
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
```

#### `data-service/.env`
```env
DATABASE_URL=postgresql://user:password@postgres:5432/cancer_db
```

#### `frontend/.env`
```env
API_GATEWAY_URL=http://api-gateway:8000
```

> ⚠️ **Important**: En production, changez les valeurs par défaut (mots de passe, secret keys)

### 3. Placement du Modèle

Placez votre modèle TensorFlow entraîné dans :
```
inference-service/models/cancer_model.h5
```

---

## 🎬 Démarrage Rapide

### Lancement Rapide

Vous avez deux options pour lancer le projet :

**Option A : Pipeline Automatisé (Recommandé)**
Ce script s'occupe de tout : nettoyage des données, entraînement du modèle et déploiement Docker.
```bash
chmod +x run_full_pipeline.sh
./run_full_pipeline.sh
```

**Option B : Lancement Manuel avec Docker**
```bash
# Construire et lancer tous les services
docker-compose up --build

# Ou en mode détaché (background)
docker-compose up -d --build
```

### Vérification des Services

```bash
# Voir les logs
docker-compose logs -f

# Vérifier le statut
docker-compose ps
```

### Accès

Une fois les services démarrés :

| Service | URL | Description |
|---------|-----|-------------|
| **Frontend** | http://localhost:8501 | Interface utilisateur |
| **API Gateway** | http://localhost:8004 | API principale |
| **Auth Service** | http://localhost:8000 | Service d'authentification |
| **Inference Service** | http://localhost:8001 | Service de prédiction |
| **Data Service** | http://localhost:8002 | Service de données |
| **PostgreSQL** | localhost:5432 | Base de données |

---

## 💻 Utilisation

### 1. Créer un Compte

1. Accédez à http://localhost:8501
2. Dans la sidebar, onglet **"Register"**
3. Entrez votre email et mot de passe
4. Cliquez sur **"S'inscrire"**

### 2. Se Connecter

1. Onglet **"Login"**
2. Entrez vos identifiants
3. Cliquez sur **"Connexion"**

### 3. Faire une Prédiction

1. Onglet **"🔍 Prédiction"**
2. Uploadez une image mammographique (JPG/PNG)
3. Cliquez sur **"🚀 Analyser l'image"**
4. Consultez le résultat avec le score de confiance

### 4. Consulter les Statistiques

Onglet **"📊 Statistiques"** :
- Total d'analyses
- Distribution Positif/Négatif
- Graphiques interactifs

### 5. Historique

Onglet **"📝 Historique"** :
- Liste complète des prédictions
- Filtrage par résultat
- Export CSV

---

## 📁 Structure du Projet

```
DL-CancerDuSein/
│
├── 📂 api-gateway/               # Service de routage
│   ├── main.py                   # Point d'entrée API Gateway
│   ├── dockerfile
│   └── requirements.txt
│
├── 📂 auth-service/              # Service d'authentification
│   ├── app/
│   │   ├── main.py               # FastAPI app
│   │   ├── models.py             # Modèles SQLAlchemy
│   │   ├── schemas.py            # Schémas Pydantic
│   │   ├── auth_utils.py         # Utilitaires JWT
│   │   └── routes/
│   ├── dockerfile
│   └── requirements.txt
│
├── 📂 inference-service/         # Service de prédiction CNN
│   ├── app/
│   │   ├── main.py
│   │   ├── route/
│   │   │   └── route.py          # Endpoints de prédiction
│   │   └── utils/
│   │       ├── model_loader.py   # Chargement du modèle
│   │       └── preprocess.py     # Prétraitement images
│   ├── models/
│   │   └── cancer_model.h5       # Modèle TensorFlow (à ajouter)
│   ├── dockerfile
│   └── requirements.txt
│
├── 📂 data-service/              # Service CRUD données
│   ├── app/
│   │   ├── main.py
│   │   ├── models.py             # Modèle Prediction
│   │   ├── schemas.py
│   │   └── routes/
│   │       ├── predictions.py    # CRUD predictions
│   │       └── stats.py          # Statistiques
│   ├── dockerfile
│   └── requirements.txt
│
├── 📂 frontend/                  # Interface Streamlit
│   ├── streamlit_app.py          # Application principale
│   ├── dockerfile
│   └── requirements.txt
│
├── 📄 docker-compose.yml         # Orchestration Docker
├── 📄 docker-compose.ngrok.yml   # Configuration avec ngrok
├── 📄 init-db.sql                # Initialisation BDD
├── 📄 expose_with_ngrok.sh       # Script ngrok
├── 📄 NGROK_GUIDE.md             # Guide ngrok
├── 📄 README.md                  # Ce fichier
└── 📄 .gitignore
```

---

## 🔌 API

### Authentification

#### `POST /api/auth/register`
Créer un nouveau compte utilisateur.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword"
}
```

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com"
}
```

#### `POST /api/auth/login`
Se connecter et obtenir un token JWT.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Prédictions

#### `POST /api/workflow/predict-and-save`
Analyser une image et sauvegarder le résultat.

**Request:**
- Type: `multipart/form-data`
- Champs: `file` (image JPG/PNG)

**Response:**
```json
{
  "prediction": {
    "prediction": "Negative",
    "confidence": 0.87
  },
  "saved_record": {
    "id": 42,
    "prediction": "Negative",
    "confidence": 0.87,
    "filename": "mammogram.jpg",
    "created_at": "2024-01-15T10:30:00"
  }
}
```

#### `GET /api/predictions`
Récupérer l'historique des prédictions.

**Query Parameters:**
- `skip`: Nombre d'éléments à sauter (default: 0)
- `limit`: Nombre maximum de résultats (default: 100)

**Response:**
```json
[
  {
    "id": 1,
    "prediction": "Positive",
    "confidence": 0.92,
    "filename": "scan1.jpg",
    "created_at": "2024-01-15T10:30:00"
  }
]
```

#### `GET /api/predictions/stats/summary`
Obtenir les statistiques globales.

**Response:**
```json
{
  "total": 150,
  "positive": 45,
  "negative": 105,
  "positive_percentage": 30.0
}
```

### Health Checks

#### `GET /health`
Vérifier l'état de chaque service.

**Response:**
```json
{
  "status": "API Gateway is running"
}
```

> 📖 Pour la documentation API complète, voir [API.md](./API.md)

---

## 🛠️ Technologies Utilisées

### Backend

| Technologie | Usage |
|------------|--------|
| **FastAPI** | Framework API REST |
| **TensorFlow** | Modèle de Deep Learning |
| **SQLAlchemy** | ORM pour PostgreSQL |
| **Pydantic** | Validation de données |
| **Python-Jose** | Gestion JWT |
| **Passlib** | Hachage de mots de passe |
| **HTTPX** | Client HTTP asynchrone |

### Frontend

| Technologie | Usage |
|------------|--------|
| **Streamlit** | Interface utilisateur |
| **Plotly** | Visualisations interactives |
| **Pandas** | Manipulation de données |
| **Pillow** | Traitement d'images |

### Infrastructure

| Technologie | Usage |
|------------|--------|
| **Docker** | Containerisation |
| **Docker Compose** | Orchestration |
| **PostgreSQL** | Base de données |
| **ngrok** | Exposition publique |

### Machine Learning

| Technologie | Usage |
|------------|--------|
| **TensorFlow/Keras** | Framework Deep Learning |
| **NumPy** | Calculs numériques |
| **PIL** | Prétraitement d'images |

---

## 🌐 Déploiement

### Développement Local

```bash
# Démarrer tous les services
docker-compose up --build
```

### Exposition Publique avec ngrok

```bash
# Installer ngrok
brew install ngrok

# Configurer le token
ngrok config add-authtoken YOUR_TOKEN

# Exposer le frontend
./ngrok_expose.sh frontend

# Ou exposer l'API
./ngrok_expose.sh api

# Ou les deux
./ngrok_expose.sh both
```

Voir le [Guide ngrok](./NGROK_GUIDE.md) pour plus de détails.

### Production

Pour un déploiement production :

1. **Sécurité**
   - Changez toutes les clés secrètes
   - Utilisez des mots de passe forts
   - Configurez HTTPS/SSL
   - Restreignez CORS

2. **Scalabilité**
   - Utilisez un load balancer
   - Déployez sur Kubernetes (optionnel)
   - Activez le monitoring (Prometheus/Grafana)

3. **Base de Données**
   - Utilisez une instance PostgreSQL managée
   - Configurez les backups automatiques
   - Activez la réplication

---

## 🐛 Troubleshooting

### Les containers ne démarrent pas

```bash
# Vérifier les logs
docker-compose logs

# Nettoyer et reconstruire
docker-compose down -v
docker-compose up --build
```

### Erreur de connexion à la base de données

```bash
# Vérifier que PostgreSQL est démarré
docker-compose ps postgres

# Recréer la base de données
docker-compose down -v
docker-compose up postgres -d
```

### Le modèle n'est pas trouvé

```bash
# Vérifier le chemin
ls inference-service/models/cancer_model.h5

# Le modèle doit être présent avant de lancer le service
```

### Port déjà utilisé

```bash
# Changer les ports dans docker-compose.yml
# Exemple: "8502:8501" au lieu de "8501:8501"
```

### Frontend ne se connecte pas à l'API

```bash
# Vérifier les variables d'environnement dans frontend/.env
# S'assurer que API_GATEWAY_URL pointe vers le bon service
```

---

## 🤝 Contribution

Les contributions sont les bienvenues ! Voici comment contribuer :

1. **Fork** le projet
2. **Créez** une branche feature (`git checkout -b feature/AmazingFeature`)
3. **Committez** vos changements (`git commit -m 'Add AmazingFeature'`)
4. **Pushez** vers la branche (`git push origin feature/AmazingFeature`)
5. **Ouvrez** une Pull Request

### Guidelines

- Suivez le style de code existant
- Ajoutez des tests pour les nouvelles fonctionnalités
- Mettez à jour la documentation
- Décrivez clairement vos changements dans la PR

---

## ⚠️ Avertissement Médical

> **IMPORTANT**: Ce système est conçu à des fins éducatives et de recherche uniquement. Il ne doit **PAS** être utilisé comme outil de diagnostic médical sans supervision d'un professionnel de la santé qualifié.
>
> - ❌ Ne remplace pas un diagnostic médical professionnel
> - ❌ Ne remplace pas une mammographie médicale
> - ✅ Peut être utilisé comme outil d'aide à la décision
> - ✅ Consultez toujours un médecin spécialiste

---

## 📄 License

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

## 👥 Auteurs

- **Votre Nom** - [GitHub](https://github.com/mnjaay)

---

## 🙏 Remerciements

- Dataset: [Breast Cancer Histopathological Database](https://web.inf.ufpr.br/vri/databases/breast-cancer-histopathological-database-breakhis/)
- TensorFlow Team
- FastAPI Framework
- Streamlit Community

---

## 📞 Support

Pour toute question ou problème :

- 📧 Email: contact@example.com
- 🐛 Issues: [GitHub Issues](https://github.com/mnjaay/DL-CancerDuSein/issues)
- 📖 Documentation: [Wiki](https://github.com/mnjaay/DL-CancerDuSein/wiki)

---

<div align="center">

**⭐ Si ce projet vous a été utile, n'hésitez pas à lui donner une étoile !**

Made with ❤️ and 🧠 by the Cancer Detection Team

</div>
