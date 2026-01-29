# 🚀 Guide de Déploiement Automatisé

Ce guide explique comment utiliser le pipeline intelligent pour entraîner, sécuriser et déployer le système de détection du cancer.

---

## 🛠️ Le Pipeline "One-Click" (Recommandé)

Nous avons consolidé l'ensemble du workflow technique dans un script maître unique. Ce script gère tout, de votre Mac jusqu'à la mise en production sur le VPS.

### 1. Lancement du Pipeline
```bash
chmod +x run_full_pipeline.sh
./run_full_pipeline.sh
```

### 2. Étapes automatisées par le script :
- **🔍 Audit de Données** : Vérifie l'intégrité des images et les répartitions (Train/Val/Test).
- **🏋️ Entraînement IA** : Lance l'apprentissage DenseNet121 et génère le fichier de mapping `classes.json`.
- **🐳 Build Docker** : Reconstruit l'image de l'Inference Service en y incluant le nouveau modèle.
- **📤 Docker Hub** : Pousse l'image vers votre registre distant (`mnjaay312/cancer-detection-inference`).
- **☁️ Déploiement VPS** : Se connecte en SSH à votre serveur et met à jour instantanément les services en ligne.

---

## 🌍 Déploiement sur le Cloud (VPS)

### Configuration Requise sur le VPS
- **Docker & Docker Compose** installés.
- **Clé SSH** configurée pour permettre au script local de piloter le serveur sans mot de passe.

### Mise à jour manuelle (si besoin)
Si vous ne souhaitez pas utiliser le script maître, vous pouvez forcer la mise à jour sur le VPS avec :
```bash
docker compose pull inference-service
docker compose up -d inference-service
```

---

## 📦 Transport du Modèle IA (Docker Hub)

Pour garantir la légèreté du repository Git et éviter les erreurs de transfert, le modèle `.h5` n'est **pas** stocké sur Git. 
- **Local** : Le modèle est généré dans `inference-service/models/`.
- **Packaging** : Lors du build Docker, le modèle est inclus directement dans l'image.
- **Production** : Le VPS télécharge l'image complète depuis Docker Hub. C'est la méthode la plus robuste pour distribuer des modèles de Deep Learning.

---

## 🐛 Résolution des Problèmes Courants

| Problème | Cause Possible | Solution |
| :--- | :--- | :--- |
| **Inversion de Résultats** | Décalage des index de classes | Résolu : Le script génère maintenant un `classes.json` dynamique. |
| **FileNotFoundError (.h5)** | Modèle manquant dans l'image | Relancez le pipeline avec l'option **(y)** pour le push Docker Hub. |
| **Erreur SSH** | Clé SSH non reconnue | Ajoutez votre clé publique sur le VPS (`ssh-copy-id root@srv1306353`). |

---

<div align="center">

**🚀 Guide de Déploiement v3.0**
Solution Cancer Detection | Automatisation Totale
Mise à jour : Janvier 2026

</div>
