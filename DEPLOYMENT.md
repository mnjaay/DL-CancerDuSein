# 🚀 Guide de Déploiement

Ce guide décrit comment déployer le système de détection du cancer dans différents environnements.

---

## Table des Matières

- [Vue d'ensemble](#vue-densemble)
- [Environnements](#environnements)
- [Déploiement Local](#déploiement-local)
- [Déploiement avec ngrok](#déploiement-avec-ngrok)
- [Déploiement sur VPS](#déploiement-sur-vps)
- [Déploiement sur Cloud](#déploiement-sur-cloud)
- [Variables d'Environnement](#variables-denvironnement)
- [Sauvegarde et Restauration](#sauvegarde-et-restauration)
- [Monitoring](#monitoring)
- [Troubleshooting](#troubleshooting)

---

## Vue d'ensemble

```mermaid
graph LR
    A[Development<br/>Local] -->|ngrok| B[Staging<br/>VPS/Cloud]
    B -->|Deploy| C[Production<br/>Cloud/K8s]
    
    style A fill:#e1f5ff
    style B fill:#fff4e1
    style C fill:#e1ffe1
```

---

## Environnements

| Environnement | Usage | Infrastructure |
|---------------|-------|----------------|
| **Development** | Développement local | Docker Compose |
| **Staging** | Tests et démos | VPS + ngrok ou Cloud VM |
| **Production** | Utilisation réelle | Cloud managed ou Kubernetes |

---

## Déploiement Local

### Prérequis

- Docker ≥ 20.10
- Docker Compose ≥ 2.0
- 8 GB RAM minimum
- 20 GB espace disque

### Installation

1. **Cloner le repository**

   ```bash
   git clone https://github.com/mnjaay/DL-CancerDuSein.git
   cd DL-CancerDuSein
   ```

2. **Placer le modèle**

   ```bash
   # Copier votre modèle TensorFlow
   cp /path/to/your/model.h5 inference-service/models/cancer_model.h5
   ```

3. **Configurer les variables (optionnel)**

   Les fichiers `.env` ont des valeurs par défaut. Pour personnaliser :

   ```bash
   # Éditer selon vos besoins
   nano auth-service/.env
   nano data-service/.env
   nano frontend/.env
   nano api-gateway/.env
   ```

4. **Lancer les services**

   ```bash
   # Construction et lancement
   docker-compose up --build

   # Ou en arrière-plan
   docker-compose up -d --build
   ```

5. **Vérifier le statut**

   ```bash
   docker-compose ps
   ```

   Tous les services doivent être "Up".

6. **Accéder à l'application**

   - Frontend: http://localhost:8501
   - API Gateway: http://localhost:8004
   - API Docs: http://localhost:8004/docs

### Arrêter les Services

```bash
# Arrêter
docker-compose stop

# Arrêter et supprimer les conteneurs
docker-compose down

# Supprimer aussi les volumes (⚠️ supprime les données)
docker-compose down -v
```

---

## Déploiement avec ngrok

### Cas d'Usage

- Exposer votre application locale sur Internet
- Faire des démos sans déploiement cloud
- Tester avec des clients externes
- Webhooks pour intégrations

### Installation ngrok

```bash
# macOS
brew install ngrok

# Linux
curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | \
  sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null && \
  echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | \
  sudo tee /etc/apt/sources.list.d/ngrok.list && \
  sudo apt update && sudo apt install ngrok

# Windows
choco install ngrok
```

### Configuration

1. **Créer un compte** sur [ngrok.com](https://ngrok.com)

2. **Obtenir votre authtoken** depuis [dashboard.ngrok.com](https://dashboard.ngrok.com/get-started/your-authtoken)

3. **Configurer l'authtoken**

   ```bash
   ngrok config add-authtoken VOTRE_TOKEN_ICI
   ```

### Utilisation

#### Option 1 : Script automatique

```bash
# Exposer le frontend
./ngrok_expose.sh frontend

# Exposer l'API
./ngrok_expose.sh api

# Exposer les deux
./ngrok_expose.sh both
```

#### Option 2 : Commandes manuelles

```bash
# Exposer le frontend (port 8501)
ngrok http 8501

# Exposer l'API Gateway (port 8004)
ngrok http 8004
```

#### Option 3 : Docker Compose avec ngrok

```bash
# Exporter votre token
export NGROK_AUTHTOKEN=your_token

# Lancer avec configuration ngrok
docker-compose -f docker-compose.ngrok.yml up
```

### Accès

Une fois ngrok lancé, vous obtiendrez une URL publique :

```
Forwarding  https://abc123-def456.ngrok.io -> http://localhost:8501
```

Partagez cette URL pour donner accès à votre application !

### Interface ngrok

Monitoring local :
```
http://localhost:4040
```

---

## Déploiement sur VPS

### Prérequis

- VPS (DigitalOcean, Linode, OVH, etc.)
- Ubuntu 22.04 LTS recommandé
- 2 vCPU minimum
- 4 GB RAM minimum
- 40 GB SSD

### Étapes

1. **Connexion SSH**

   ```bash
   ssh root@VOTRE_IP_VPS
   ```

2. **Installer Docker**

   ```bash
   # Mettre à jour le système
   apt update && apt upgrade -y

   # Installer Docker
   curl -fsSL https://get.docker.com -o get-docker.sh
   sh get-docker.sh

   # Installer Docker Compose
   apt install docker-compose-plugin -y

   # Vérifier
   docker --version
   docker compose version
   ```

3. **Cloner le repository**

   ```bash
   git clone https://github.com/mnjaay/DL-CancerDuSein.git
   cd DL-CancerDuSein
   ```

4. **Transférer le modèle**

   Depuis votre machine locale :

   ```bash
   scp cancer_model.h5 root@VOTRE_IP_VPS:/root/DL-CancerDuSein/inference-service/models/
   ```

5. **Configurer les variables d'environnement**

   ```bash
   # Exemple pour auth-service
   nano auth-service/.env
   ```

   **⚠️ Important** : Changez les valeurs par défaut en production !

   ```env
   DATABASE_URL=postgresql://user:STRONG_PASSWORD@postgres:5432/auth_db
   SECRET_KEY=GENERATE_A_STRONG_RANDOM_SECRET
   ALGORITHM=HS256
   ```

6. **Lancer les services**

   ```bash
   docker compose up -d --build
   ```

7. **Vérifier les logs**

   ```bash
   docker compose logs -f
   ```

8. **Exposer avec ngrok (optionnel)**

   ```bash
   # Installer ngrok sur le VPS
   curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | \
     sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null && \
     echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | \
     sudo tee /etc/apt/sources.list.d/ngrok.list && \
     sudo apt update && sudo apt install ngrok

   # Configurer
   ngrok config add-authtoken VOTRE_TOKEN

   # Exposer (dans un screen ou tmux)
   ngrok http 8501
   ```

### Firewall

Si vous n'utilisez pas ngrok, ouvrez les ports :

```bash
# UFW (Ubuntu)
ufw allow 8501/tcp  # Frontend
ufw allow 8004/tcp  # API Gateway
ufw allow 22/tcp    # SSH
ufw enable
```

---

## Déploiement sur Cloud

### AWS (Amazon Web Services)

#### Architecture Recommandée

```mermaid
graph TB
    ALB[Application Load Balancer] --> ECS[ECS Fargate]
    ECS --> RDS[(RDS PostgreSQL)]
    ECS --> S3[S3 Storage]
    
    style ALB fill:#ff9900
    style ECS fill:#ff9900
    style RDS fill:#3b48cc
    style S3 fill:#569a31
```

#### Services AWS

- **Compute** : ECS Fargate ou EC2
- **Database** : RDS PostgreSQL
- **Storage** : S3 (pour modèles)
- **Load Balancer** : ALB
- **Monitoring** : CloudWatch

#### Déploiement ECS

1. **Créer un ECR repository**

   ```bash
   aws ecr create-repository --repository-name cancer-detection-frontend
   aws ecr create-repository --repository-name cancer-detection-api
   aws ecr create-repository --repository-name cancer-detection-inference
   ```

2. **Build et push les images**

   ```bash
   # Login
   aws ecr get-login-password --region us-east-1 | \
     docker login --username AWS --password-stdin ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com

   # Build
   docker build -t cancer-detection-frontend ./frontend
   docker tag cancer-detection-frontend:latest ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/cancer-detection-frontend:latest

   # Push
   docker push ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/cancer-detection-frontend:latest
   ```

3. **Créer une task definition ECS**

4. **Créer un service ECS**

5. **Configurer l'ALB**

### Google Cloud Platform (GCP)

#### Services GCP

- **Compute** : Cloud Run
- **Database** : Cloud SQL (PostgreSQL)
- **Storage** : Cloud Storage
- **Load Balancer** : Cloud Load Balancing

#### Déploiement Cloud Run

```bash
# Build avec Cloud Build
gcloud builds submit --tag gcr.io/PROJECT_ID/frontend

# Deploy
gcloud run deploy frontend \
  --image gcr.io/PROJECT_ID/frontend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### Azure

#### Services Azure

- **Compute** : Azure Container Instances ou AKS
- **Database** : Azure Database for PostgreSQL
- **Storage** : Azure Blob Storage

---

## Variables d'Environnement

### Configuration Complète

#### `api-gateway/.env`

```env
AUTH_SERVICE_URL=http://auth-service:8000
INFERENCE_SERVICE_URL=http://inference-service:8001
DATA_SERVICE_URL=http://data-service:8002
```

#### `auth-service/.env`

```env
# Database
DATABASE_URL=postgresql://user:password@postgres:5432/auth_db

# JWT
SECRET_KEY=your-secret-key-min-32-characters
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**Générer une secret key** :
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

#### `data-service/.env`

```env
DATABASE_URL=postgresql://user:password@postgres:5432/cancer_db
```

#### `frontend/.env`

```env
API_GATEWAY_URL=http://api-gateway:8000
```

### Production : Bonnes Pratiques

1. **Ne jamais commiter les `.env`**

   Vérifiez `.gitignore` :
   ```
   .env
   *.env
   ```

2. **Utiliser un gestionnaire de secrets**

   - AWS : Secrets Manager
   - GCP : Secret Manager
   - Azure : Key Vault
   - HashiCorp Vault

3. **Différentes valeurs par environnement**

   ```
   .env.development
   .env.staging
   .env.production
   ```

---

## Sauvegarde et Restauration

### Sauvegarde de la Base de Données

#### Automatique (avec cron)

```bash
# Script de sauvegarde
#!/bin/bash
# backup.sh

BACKUP_DIR="/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

docker exec postgres pg_dump -U user cancer_db > \
  $BACKUP_DIR/cancer_db_$TIMESTAMP.sql

docker exec postgres pg_dump -U user auth_db > \
  $BACKUP_DIR/auth_db_$TIMESTAMP.sql

# Supprimer les backups > 7 jours
find $BACKUP_DIR -name "*.sql" -mtime +7 -delete
```

```bash
# Rendre exécutable
chmod +x backup.sh

# Ajouter au cron (tous les jours à 2h)
crontab -e
# 0 2 * * * /path/to/backup.sh
```

### Restauration

```bash
# Restaurer cancer_db
cat backup.sql | docker exec -i postgres psql -U user -d cancer_db

# Ou
docker exec -i postgres psql -U user -d cancer_db < backup.sql
```

---

## Monitoring

### Health Checks

```bash
# Script de monitoring
#!/bin/bash

SERVICES=("http://localhost:8501" "http://localhost:8004" "http://localhost:8000")

for service in "${SERVICES[@]}"; do
  STATUS=$(curl -s -o /dev/null -w "%{http_code}" $service)
  if [ $STATUS -eq 200 ]; then
    echo "✅ $service is up"
  else
    echo "❌ $service is down (status: $STATUS)"
  fi
done
```

### Logs

```bash
# Voir tous les logs
docker compose logs

# Logs d'un service spécifique
docker compose logs frontend

# Suivre les logs en temps réel
docker compose logs -f

# Logs des dernières 100 lignes
docker compose logs --tail=100
```

### Prometheus + Grafana (Avancé)

Ajoutez à `docker-compose.yml` :

```yaml
prometheus:
  image: prom/prometheus
  volumes:
    - ./prometheus.yml:/etc/prometheus/prometheus.yml
  ports:
    - "9090:9090"

grafana:
  image: grafana/grafana
  ports:
    - "3000:3000"
  environment:
    - GF_SECURITY_ADMIN_PASSWORD=admin
```

---

## Troubleshooting

### Problèmes Courants

#### Les services ne démarrent pas

```bash
# Voir les erreurs
docker compose logs

# Vérifier les ressources
docker stats
```

#### Erreur de connexion à PostgreSQL

```bash
# Vérifier que PostgreSQL est démarré
docker compose ps postgres

# Voir les logs PostgreSQL
docker compose logs postgres

# Redémarrer PostgreSQL
docker compose restart postgres
```

#### Le modèle n'est pas trouvé

```bash
# Vérifier la présence du fichier
ls -lh inference-service/models/cancer_model.h5

# Si absent, le copier
cp /path/to/model.h5 inference-service/models/cancer_model.h5

# Redémarrer le service
docker compose restart inference-service
```

#### Port déjà utilisé

```bash
# Trouver le processus utilisant le port
lsof -i :8501

# Tuer le processus
kill -9 PID

# Ou changer le port dans docker-compose.yml
ports:
  - "8502:8501"  # Utiliser 8502 au lieu de 8501
```

#### Manque de mémoire

```bash
# Augmenter la mémoire Docker (Docker Desktop)
# Settings > Resources > Memory

# Ou limiter les ressources des services
services:
  inference-service:
    deploy:
      resources:
        limits:
          memory: 2G
```

---

## Checklist de Déploiement Production

- [ ] Changer tous les mots de passe par défaut
- [ ] Générer une nouvelle SECRET_KEY
- [ ] Configurer HTTPS/SSL
- [ ] Restreindre CORS aux domaines autorisés
- [ ] Mettre en place les sauvegardes automatiques
- [ ] Configurer le monitoring
- [ ] Tester tous les endpoints
- [ ] Documenter les procédures d'urgence
- [ ] Configurer les alertes
- [ ] Ajouter rate limiting
- [ ] Configurer les logs centralisés

---

## Support

Pour de l'aide supplémentaire :

- 📖 [Documentation complète](./README.md)
- 🐛 [Issues GitHub](https://github.com/mnjaay/DL-CancerDuSein/issues)
- 📧 Email : support@example.com

---

<div align="center">

**🚀 Guide de Déploiement - Cancer Detection System**

Bonne chance avec votre déploiement !

</div>
