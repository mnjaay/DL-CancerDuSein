# 🚀 Guide de Déploiement

Ce guide décrit comment déployer et automatiser le système de détection du cancer.

---

## 🛠️ Automatisation Locale (Recommandé)

Le déploiement manuel a été remplacé par un script maître qui automatise tout le workflow :

```bash
# 1. Rendre le script exécutable
chmod +x run_full_pipeline.sh

# 2. Lancer le pipeline complet
./run_full_pipeline.sh
```

**Ce script effectue :**
1. 🔧 Installation de l'environnement virtuel (`venv`).
2. 🔍 **Vérification des données** : Détecte si les données sont prêtes ou s'il faut les diviser.
3. 🏋️ Entraînement du nouveau modèle **DenseNet121** (`model.h5`).
4. 🐳 Reconstruction du service d'inférence Docker.

---

## 🐳 Déploiement Docker Classique

Si vous souhaitez simplement lancer les services sans ré-entraîner le modèle :

```bash
# Construction et lancement
docker-compose up -d --build
```

**Accès :**
- **Frontend** : [http://localhost:8501](http://localhost:8501)
- **API Gateway** : [http://localhost:8004](http://localhost:8004)
- **Stats & Historique** : Disponibles dans l'interface Streamlit.

---

## 🔄 CI/CD et Modèles Volumineux

### 🐘 Git LFS (Large File Storage)
Étant donné que les modèles `.h5` dépassent souvent les limites de Git, nous utilisons **Git LFS**.
Avant tout `git push`, assurez-vous que LFS est actif :
```bash
git lfs install
git lfs track "*.h5"
```

### 🤖 GitHub Actions
Le déploiement est automatisé via `.github/workflows/model-update.yml`. 
Dès qu'un fichier `.h5` est détecté dans un commit sur `main` :
1. GitHub lance un serveur de build.
2. L'image Docker de l'Inference Service est reconstruite.
3. L'image est poussée sur votre Docker Hub pour mise à jour automatique.

---

## ☁️ Déploiement Cloud (Production)

### VPS (DigitalOcean, Linode, AWS EC2)
1. Installez Docker et Docker Compose.
2. Clonez le repository.
3. Utilisez le script maître ou lancez Docker Compose.

### HTTPS & DNS
Pour la production, il est recommandé d'utiliser un **Reverse Proxy** (Nginx ou Traefik) pour gérer le SSL via **Let's Encrypt**.

---

## 🐛 Troubleshooting

| Problème | Solution |
| :--- | :--- |
| `SameFileError` | Le pipeline détecte désormais si les données sont déjà organisées pour éviter ce conflit. |
| `Out of Memory` | Augmentez la mémoire allouée à Docker Desktop (> 8GB) pour l'entraînement local. |
| Erreur BDD | Relancez les conteneurs ou vérifiez les logs (`docker logs`). |

---

<div align="center">

**🚀 Guide de Déploiement v2.1**
Solution Cancer Detection
Version Janvier 2026
</div>
