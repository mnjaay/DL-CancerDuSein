# 🏗️ Architecture du Système

## Vue d'ensemble

Ce document décrit l'architecture complète du système de détection du cancer du sein, basée sur une **architecture microservices** moderne et scalable.

---

## Table des Matières

- [Principes Architecturaux](#principes-architecturaux)
- [Architecture Globale](#architecture-globale)
- [Services Détaillés](#services-détaillés)
- [Base de Données](#base-de-données)
- [Communication Inter-Services](#communication-inter-services)
- [Flux de Données](#flux-de-données)
- [Sécurité](#sécurité)
- [Scalabilité](#scalabilité)
- [Déploiement](#déploiement)

---

## Principes Architecturaux

### 🎯 Objectifs

1. **Séparation des Responsabilités** : Chaque service a une fonction unique
2. **Scalabilité** : Services indépendants pouvant être scalés séparément
3. **Maintenabilité** : Code modulaire et facile à maintenir
4. **Résilience** : Isolation des pannes
5. **Performance** : Architecture asynchrone et optimisée

### 🏛️ Patterns Utilisés

- **API Gateway Pattern** : Point d'entrée unique
- **Database per Service** : Chaque service a sa propre base de données
- **Microservices Pattern** : Services indépendants et déployables
- **Container Pattern** : Tous les services sont containerisés

---

## Architecture Globale

```mermaid
graph TB
    subgraph "External Layer"
        U[👤 Utilisateur/Client]
        N[🌐 ngrok<br/>Tunnel Public]
    end
    
    subgraph "Presentation Layer"
        F[🎨 Frontend Service<br/>Streamlit<br/>Port: 8501]
    end
    
    subgraph "Gateway Layer"
        G[🚪 API Gateway<br/>FastAPI<br/>Port: 8004]
    end
    
    subgraph "Business Logic Layer"
        A[🔐 Auth Service<br/>FastAPI<br/>Port: 8000]
        I[🧠 Inference Service<br/>TensorFlow + FastAPI<br/>Port: 8001]
        D[💾 Data Service<br/>FastAPI + SQLAlchemy<br/>Port: 8002]
    end
    
    subgraph "Data Layer"
        DB[(🗄️ PostgreSQL<br/>Port: 5432)]
    end
    
    subgraph "ML Layer"
        M[🤖 CNN Model<br/>TensorFlow/Keras<br/>cancer_model.h5]
    end
    
    U -->|HTTPS| N
    N -->|HTTP| F
    U -.->|Development| F
    F -->|API Calls| G
    
    G -->|Auth Requests| A
    G -->|Prediction Requests| I
    G -->|CRUD Requests| D
    
    A -->|SQL| DB
    D -->|SQL| DB
    I -->|Load Model| M
    I -.->|Save Results| D
    
    style U fill:#e1f5ff
    style N fill:#fff9e1
    style F fill:#e1f5ff
    style G fill:#fff4e1
    style A fill:#ffe1f5
    style I fill:#e1ffe1
    style D fill:#f5e1ff
    style DB fill:#ffe1e1
    style M fill:#e1ffe1
```

---

## Services Détaillés

### 🎨 Frontend Service

**Responsabilité** : Interface utilisateur

**Technologies** :
- Streamlit 1.28+
- Plotly (visualisations)
- Pandas (manipulation de données)
- Requests (HTTP client)

**Fonctionnalités** :
- Authentification utilisateur (Login/Register)
- Upload d'images
- Affichage des résultats de prédiction
- Visualisations interactives (graphiques)
- Historique des analyses
- Export CSV

**Configuration** :
```python
API_GATEWAY_URL = os.getenv("API_GATEWAY_URL", "http://api-gateway:8000")
```

**Structure** :
```
frontend/
├── streamlit_app.py    # Application principale
├── requirements.txt
├── dockerfile
└── .env
```

---

### 🚪 API Gateway

**Responsabilité** : Point d'entrée unique, routage des requêtes

**Technologies** :
- FastAPI
- HTTPX (client HTTP asynchrone)
- CORS Middleware

**Fonctionnalités** :
- Routage vers les services appropriés
- Gestion CORS
- Health checks
- Workflow combiné (predict-and-save)

**Endpoints** :
```python
# Auth proxy
POST   /api/auth/register
POST   /api/auth/login
GET    /api/auth/verify

# Inference proxy
POST   /api/inference/predict

# Data proxy
GET    /api/predictions
POST   /api/predictions
GET    /api/predictions/{id}
PUT    /api/predictions/{id}
DELETE /api/predictions/{id}
GET    /api/predictions/stats/summary

# Workflow
POST   /api/workflow/predict-and-save

# Health
GET    /health
```

**Architecture** :

```mermaid
graph LR
    C[Client] -->|Request| G[API Gateway]
    G -->|Route| A[Auth Service]
    G -->|Route| I[Inference Service]
    G -->|Route| D[Data Service]
    
    A -->|Response| G
    I -->|Response| G
    D -->|Response| G
    G -->|Response| C
```

**Configuration** :
```python
AUTH_SERVICE_URL = "http://auth-service:8000"
INFERENCE_SERVICE_URL = "http://inference-service:8001"
DATA_SERVICE_URL = "http://data-service:8002"
```

---

### 🔐 Auth Service

**Responsabilité** : Gestion de l'authentification et des utilisateurs

**Technologies** :
- FastAPI
- SQLAlchemy (ORM)
- Passlib (hachage de mots de passe avec Argon2)
- Python-Jose (JWT)
- PostgreSQL

**Modèle de Données** :
```python
class User:
    id: int
    email: str (unique, index)
    hashed_password: str
    created_at: datetime
```

**Fonctionnalités** :
- Inscription utilisateur
- Connexion (génération JWT)
- Vérification de token
- Hachage sécurisé des mots de passe (Argon2)

**Sécurité** :
- Mots de passe jamais stockés en clair
- Tokens JWT avec expiration
- Email unique par utilisateur

**Endpoints** :
```python
POST /auth/register      # Créer un compte
POST /auth/login         # Se connecter
GET  /auth/verify        # Vérifier un token
```

**Configuration** :
```env
DATABASE_URL=postgresql://user:password@postgres:5432/auth_db
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
```

---

### 🧠 Inference Service

**Responsabilité** : Prédictions avec le modèle CNN

**Technologies** :
- FastAPI
- TensorFlow 2.x
- NumPy
- Pillow (traitement d'images)

**Modèle** :
- Type : CNN (Convolutional Neural Network)
- Framework : TensorFlow/Keras
- Fichier : `models/cancer_model.h5`
- Input : Images 224x224 RGB
- Output : Score binaire (0-1)

**Pipeline de Prédiction** :

```mermaid
graph LR
    A[Image Upload] --> B[Prétraitement]
    B --> C[Resize 224x224]
    C --> D[Normalisation]
    D --> E[CNN Model]
    E --> F[Score 0-1]
    F --> G[Classification]
    G --> H[Positive/Negative]
    
    style E fill:#e1ffe1
```

**Prétraitement** :
```python
def preprocess_image(image: Image) -> np.ndarray:
    # Resize to 224x224
    image = image.resize((224, 224))
    # Convert to RGB
    image = image.convert("RGB")
    # To array and normalize
    image_array = np.array(image) / 255.0
    # Add batch dimension
    return np.expand_dims(image_array, axis=0)
```

**Classification** :
```python
prediction_score = model.predict(image_array)[0][0]
predicted_class = "Positive" if prediction_score >= 0.5 else "Negative"
confidence = prediction_score if prediction_score >= 0.5 else 1 - prediction_score
```

**Endpoints** :
```python
POST /inference/predict  # Analyser une image
GET  /                   # Health check
```

---

### 💾 Data Service

**Responsabilité** : CRUD des prédictions et statistiques

**Technologies** :
- FastAPI
- SQLAlchemy (ORM)
- PostgreSQL

**Modèle de Données** :
```python
class Prediction:
    id: int (primary key)
    prediction: str ("Positive" ou "Negative")
    confidence: float (0.0 - 1.0)
    filename: str
    created_at: datetime
```

**Fonctionnalités** :
- Créer une prédiction
- Lire les prédictions (pagination)
- Mettre à jour une prédiction
- Supprimer une prédiction
- Statistiques globales

**Endpoints** :
```python
POST   /predictions/              # Créer
GET    /predictions/              # Lire toutes (pagination)
GET    /predictions/{id}          # Lire une
PUT    /predictions/{id}          # Mettre à jour
DELETE /predictions/{id}          # Supprimer
GET    /predictions/stats/summary # Statistiques
GET    /health                    # Health check
```

**Statistiques** :
```python
{
    "total": int,               # Nombre total
    "positive": int,            # Cas positifs
    "negative": int,            # Cas négatifs
    "positive_percentage": float # Pourcentage positif
}
```

---

### 🗄️ PostgreSQL Database

**Configuration** :
```yaml
Image: postgres:15
User: user
Password: password
Port: 5432
```

**Bases de Données** :

1. **auth_db** : Données d'authentification
   - Table : `users`

2. **cancer_db** : Données de prédictions
   - Table : `predictions`

**Initialisation** :
```sql
CREATE DATABASE auth_db;
CREATE DATABASE cancer_db;
GRANT ALL PRIVILEGES ON DATABASE auth_db TO "user";
GRANT ALL PRIVILEGES ON DATABASE cancer_db TO "user";
```

**Schéma** :

```mermaid
erDiagram
    USERS {
        int id PK
        string email UK
        string hashed_password
        datetime created_at
    }
    
    PREDICTIONS {
        int id PK
        string prediction
        float confidence
        string filename
        datetime created_at
    }
```

---

## Communication Inter-Services

### Transport

- **Protocole** : HTTP/REST
- **Format** : JSON
- **Client** : HTTPX (asynchrone)

### Patterns de Communication

#### 1. Request-Response (Synchrone)

```mermaid
sequenceDiagram
    participant C as Client
    participant G as Gateway
    participant S as Service
    
    C->>G: HTTP Request
    G->>S: Forward Request
    S-->>G: Response
    G-->>C: Forward Response
```

#### 2. Workflow Combiné

```mermaid
sequenceDiagram
    participant C as Client
    participant G as Gateway
    participant I as Inference
    participant D as Data Service
    
    C->>G: POST /workflow/predict-and-save
    G->>I: POST /inference/predict
    I-->>G: Prediction Result
    G->>D: POST /predictions
    D-->>G: Saved Record
    G-->>C: Combined Response
```

### Service Discovery

Les services se découvrent via **noms de conteneurs Docker** :
```python
AUTH_SERVICE_URL = "http://auth-service:8000"
INFERENCE_SERVICE_URL = "http://inference-service:8001"
DATA_SERVICE_URL = "http://data-service:8002"
```

Docker Compose crée automatiquement un réseau interne où les services peuvent communiquer par nom.

---

## Flux de Données

### 1. Flux d'Authentification

```mermaid
sequenceDiagram
    participant U as User
    participant F as Frontend
    participant G as Gateway
    participant A as Auth Service
    participant DB as PostgreSQL
    
    U->>F: Enter credentials
    F->>G: POST /api/auth/login
    G->>A: POST /auth/login
    A->>DB: SELECT user
    DB-->>A: User data
    A->>A: Verify password
    A->>A: Generate JWT
    A-->>G: JWT Token
    G-->>F: JWT Token
    F->>F: Store token
    F-->>U: Login success
```

### 2. Flux de Prédiction Complète

```mermaid
sequenceDiagram
    participant U as User
    participant F as Frontend
    participant G as Gateway
    participant I as Inference
    participant M as CNN Model
    participant D as Data Service
    participant DB as PostgreSQL
    
    U->>F: Upload image
    F->>G: POST /api/workflow/predict-and-save
    G->>I: POST /inference/predict
    I->>I: Preprocess image
    I->>M: Predict
    M-->>I: Score
    I->>I: Classify
    I-->>G: {prediction, confidence}
    G->>D: POST /predictions
    D->>DB: INSERT prediction
    DB-->>D: Saved record
    D-->>G: Record data
    G-->>F: Combined result
    F-->>U: Display result
```

### 3. Flux de Récupération des Statistiques

```mermaid
sequenceDiagram
    participant U as User
    participant F as Frontend
    participant G as Gateway
    participant D as Data Service
    participant DB as PostgreSQL
    
    U->>F: View statistics
    F->>G: GET /api/predictions/stats/summary
    G->>D: GET /predictions/stats/summary
    D->>DB: SELECT COUNT(*)...
    DB-->>D: Aggregated data
    D->>D: Calculate percentages
    D-->>G: Statistics
    G-->>F: Statistics
    F->>F: Create charts
    F-->>U: Display charts
```

---

## Sécurité

### Authentification

- **Méthode** : JWT (JSON Web Tokens)
- **Algorithme** : HS256
- **Storage** : Session state (Frontend)

### Hachage des Mots de Passe

- **Algorithme** : Argon2 (via Passlib)
- **Avantages** : Résistant aux attaques GPU/ASIC

```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
hashed_password = pwd_context.hash(plain_password)
```

### CORS

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ⚠️ Restreindre en production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Variables d'Environnement

Toutes les informations sensibles sont dans `.env` :
- Mots de passe de base de données
- Clés secrètes JWT
- URLs de services

### Recommandations Production

1. **HTTPS uniquement**
2. **Restreindre CORS** à des domaines spécifiques
3. **Secrets Manager** (AWS Secrets Manager, HashiCorp Vault)
4. **Rate Limiting**
5. **API Keys** pour les clients externes
6. **Audit Logging**

---

## Scalabilité

### Scalabilité Horizontale

Chaque service peut être scalé indépendamment :

```yaml
docker-compose up --scale inference-service=3
```

### Load Balancing

Pour production, ajoutez un load balancer (NGINX, Traefik) :

```mermaid
graph TB
    C[Client] --> LB[Load Balancer]
    LB --> G1[Gateway 1]
    LB --> G2[Gateway 2]
    LB --> G3[Gateway 3]
    
    G1 --> I1[Inference 1]
    G2 --> I2[Inference 2]
    G3 --> I3[Inference 3]
```

### Optimisations

1. **Caching** : Redis pour les résultats fréquents
2. **CDN** : Pour les assets statiques
3. **Database Pooling** : Connexions réutilisables
4. **Async I/O** : FastAPI et HTTPX (déjà implémenté)

### Bottlenecks

- **Inference Service** : Limité par le GPU/CPU pour les prédictions
- **PostgreSQL** : Peut nécessiter une instance plus puissante

### Solutions

- **GPU** : Déployer Inference Service sur instance avec GPU
- **Database** : PostgreSQL managé avec autoscaling (RDS, Cloud SQL)
- **Queue** : Celery + Redis pour prédictions asynchrones

---

## Déploiement

### Architecture de Déploiement

```mermaid
graph TB
    subgraph "Development"
        D1[Docker Compose<br/>Local Machine]
    end
    
    subgraph "Staging"
        D2[Docker Compose<br/>Cloud VM]
        N2[ngrok Tunnel]
    end
    
    subgraph "Production"
        K8S[Kubernetes Cluster]
        LB[Load Balancer]
        RDS[(Managed PostgreSQL)]
        S3[Object Storage]
    end
    
    D1 -.->|Push| D2
    D2 -->|Public URL| N2
    D2 -.->|Deploy| K8S
    K8S --> LB
    K8S --> RDS
    K8S --> S3
```

### Environnements

#### Development (Local)

```bash
docker-compose up --build
```

#### Staging (Cloud VM)

```bash
# Sur une VM cloud (AWS EC2, GCP Compute Engine)
docker-compose up -d
./ngrok_expose.sh both
```

#### Production (Kubernetes)

```yaml
# Exemple minimal
apiVersion: apps/v1
kind: Deployment
metadata:
  name: inference-service
spec:
  replicas: 3
  selector:
    matchLabels:
      app: inference
  template:
    metadata:
      labels:
        app: inference
    spec:
      containers:
      - name: inference
        image: cancer-detection/inference:latest
        ports:
        - containerPort: 8001
        resources:
          limits:
            nvidia.com/gpu: 1  # GPU support
```

### CI/CD Pipeline

```mermaid
graph LR
    A[Git Push] --> B[GitHub Actions]
    B --> C[Build Docker Images]
    C --> D[Run Tests]
    D --> E[Push to Registry]
    E --> F[Deploy to Staging]
    F --> G{Manual Approval}
    G -->|Approved| H[Deploy to Production]
```

---

## Monitoring & Observabilité

### Logs

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### Metrics (Recommandé)

- **Prometheus** : Collecte de métriques
- **Grafana** : Visualisation
- **Metrics à surveiller** :
  - Nombre de prédictions/minute
  - Latence moyenne des prédictions
  - Taux d'erreur
  - Utilisation CPU/GPU

### Tracing (Recommandé)

- **Jaeger** ou **Zipkin**
- Tracer les requêtes à travers les microservices

---

## Évolutions Futures

### Phase 2

- [ ] Gestion des rôles (Admin, Doctor, Patient)
- [ ] Upload d'images DICOM
- [ ] Historique par utilisateur
- [ ] API versioning (v2)

### Phase 3

- [ ] Monitoring avec Prometheus + Grafana
- [ ] CI/CD complet
- [ ] Tests automatisés (pytest)
- [ ] Documentation OpenAPI enrichie

### Phase 4

- [ ] Multi-modèles (différents types de cancer)
- [ ] Explainability (Grad-CAM)
- [ ] Mobile app (React Native)
- [ ] Intégration HL7/FHIR

---

## Références

- [Microservices Pattern](https://microservices.io/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [TensorFlow Serving](https://www.tensorflow.org/tfx/guide/serving)

---

<div align="center">

**🏗️ Architecture Documentation - Cancer Detection System**

Version 1.0 | Dernière mise à jour : Janvier 2024

</div>
