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
2. 🧹 Nettoyage des images brutes dans `ml/data/raw`.
3. 🏋️ Entraînement du nouveau modèle (`model.h5`).
4. 🐳 Reconstruction et redémarrage des conteneurs Docker.

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
| `ReadTimeoutError` | Augmentez `HTTPX_TIMEOUT` dans `api-gateway/main.py` si le modèle est très complexe. |
| `Out of Memory` | Augmentez la mémoire allouée à Docker Desktop (> 8GB). |
| Erreur BDD | Lancez `docker-compose down -v` pour réinitialiser les schémas (⚠️ Attention aux données). |

---

<div align="center">

**🚀 Guide de Déploiement v2.0**
Solution Cancer Detection

</div>
