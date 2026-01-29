# 🚀 Manuel de Déploiement et Opérations Cloud

Ce guide détaille la procédure de mise en production et de maintenance du système sur un VPS (Virtual Private Server).

---

## 📡 1. Stratégie de Déploiement "Zero-Down-Time"

### Le Pipeline Séquentiel
Le script `run_full_pipeline.sh` implémente le workflow suivant :
1. **Audit** : Validation des datasets ML.
2. **Train** : Génération du modèle `.h5` et du `classes.json`.
3. **Packaging** : Injection des artefacts IA dans l'image Docker de l'Inference Service.
4. **Push** : Publication sur **Docker Hub**.
5. **Sync** : Notification SSH au VPS pour déclencher le `pull` et le `restart`.

---

## 🔒 2. Gestion de la Sécurité SSL (Production)

### Configuration Certbot
Sur le VPS Hostinger, les certificats sont générés une seule fois :
```bash
# Commande pour générer les certificats (Nginx doit être stoppé temporairement)
sudo certbot certonly --standalone -d cancer-detection.myftp.org
```

### Mécanisme de Bascule (Switch)
Comme le fichier `docker-compose.yml` et `nginx.conf` diffèrent entre le développement local et la production, nous utilisons les backups :
- **Sur le VPS** : Toujours exécuter `cp nginx/nginx.conf.prod nginx/nginx.conf` après un `git pull`.
- **Ports** : Assurez-vous que le port **443** est ouvert dans le pare-feu du VPS (UFW ou console Hostinger).

---

## 🛠️ 3. Commandes de Maintenance Utiles

### Vérification des Logs
```bash
# Voir les logs du moteur IA en direct
docker compose logs -f inference-service

# Voir les erreurs de redirection Nginx
docker compose logs nginx
```

### Mise à jour d'un service spécifique
```bash
# Mettre à jour uniquement le frontend sans couper le reste
git pull
docker compose up -d --build frontend
```

### Nettoyage du Serveur
```bash
# Libérer de l'espace disque sur le VPS (supprime les anciennes images)
docker system prune -f
```

---

## 📋 4. Checklist Post-Déploiement
- [ ] Accès HTTPS fonctionnel (cadenas vert).
- [ ] Redirection HTTP -> HTTPS active.
- [ ] Upload d'image de 5 Mo réussi (test client_max_body_size).
- [ ] Historique des prédictions persistant après redémarrage.

---

<div align="center">
  
**Guide Opérationnel v4.0**  
*Ingénierie DevOps & IA*

</div>
