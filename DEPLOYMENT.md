# 🚀 Guide de Déploiement & Sécurisation

Ce guide détaille les étapes pour déployer le système en production avec une sécurité maximale.

---

## 🛠️ Pipeline "One-Click"
Le script `run_full_pipeline.sh` automatise :
1. L'audit des données.
2. L'entraînement IA.
3. Le packaging Docker du modèle (Docker Hub).
4. Le déploiement SSH sur le VPS.

---

## 🔒 Activation HTTPS (SSL)
Le système utilise **Let's Encrypt** pour sécuriser les communications.

### 1. Prérequis sur le VPS
Le domaine doit être configuré (ex: `cancer-detection.myftp.org`).
Installez Certbot sur le VPS :
```bash
sudo apt update && sudo apt install -y certbot
```

### 2. Génération du Certificat
Le port 80 doit être libre (arrêtez Nginx si besoin) :
```bash
docker compose stop nginx
sudo certbot certonly --standalone -d cancer-detection.myftp.org
```

### 3. Basculement Production
Une fois le certificat généré :
1. Activez les lignes SSL dans `docker-compose.yml` (Ports 443 et volume `/etc/letsencrypt`).
2. Utilisez le fichier `nginx/nginx.conf.prod` (copiez-le vers `nginx/nginx.conf`).
3. Relancez : `docker compose up -d --build nginx`.

---

## 💻 Développement Local
Si vous travaillez sur votre Mac, le SSL ne fonctionnera pas (pas de certificats locaux).
**Pour revenir en mode local :**
1. Commentez les lignes SSL dans `docker-compose.yml`.
2. Utilisez la version simple de `nginx/nginx.conf` (sans SSL).
3. Accédez à `http://localhost`.

---

## 🐛 Résolution des Problèmes
| Problème | Solution |
| :--- | :--- |
| **Erreur SSL Nginx** | Vérifiez que le volume `/etc/letsencrypt` est bien monté dans `docker-compose.yml`. |
| **Upload bloqué** | Nginx est configuré à 50Mo. Si besoin, augmentez `client_max_body_size` dans `nginx.conf`. |
| **Erreur API Invalide** | Consultez les logs du Gateway : `docker compose logs api-gateway`. |

---

<div align="center">
**Guide de Déploiement v3.5** | Janvier 2026
</div>
