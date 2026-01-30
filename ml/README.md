# 🤖 Guide d'Entraînement Deep Learning

Ce dossier contient l'expertise et les outils nécessaires pour entraîner le modèle de vision par ordinateur et valider ses performances sur des mammographies numériques.

---

## 🚀 Pipeline d'Entraînement

### 1. Préparation de l'Environnement
Il est fortement recommandé d'utiliser le script de configuration à la racine pour isoler les dépendances :
```bash
# À la racine du projet
./setup_ml.sh
source ml/venv/bin/activate
cd ml
```

### 2. Organisation des Données
Le système s'attend à ce que les données soient déjà réparties en trois sous-dossiers (`train`, `val`, `test`), chacun contenant les classes d'images :
```text
ml/data/
├── train/
│   ├── Positive/
│   └── Negative/
├── val/
│   ├── Positive/
│   └── Negative/
└── test/
    ├── Positive/
    └── Negative/
```

### 3. Vérification de l'Intégrité
Avant de lancer l'entraînement, vérifiez que vos données sont correctement structurées et lisibles par TensorFlow :
```bash
python preprocessing.py check --data_dir data
```

### 4. Entraînement & Évaluation Automatisée
Le script déclenche l'apprentissage et une évaluation finale sur l'ensemble de test :
```bash
python train.py --config config.yaml
```
*Le modèle est automatiquement validé et sauvegardé dans `../inference-service/models/model.h5`.*

---

## ⚙️ Détails Techniques

### Architecture : DenseNet-121
Nous utilisons une architecture **DenseNet-121** (Dense Convolutional Network) pour sa capacité supérieure en réutilisation de caractéristiques, cruciale pour détecter les motifs subtils des tissus mammaires.
- **Fine-tuning** : Base pré-entraînée sur ImageNet avec déblocage progressif des couches.
- **Optimisation** : Adam optimizer avec réduction dynamique du taux d'apprentissage.

### Configuration (`config.yaml`)
Personnalisation sans modification du code source :
- **Model** : Dimensions d'entrée (128x128x3).
- **Training** : Batch size, Époques (Early Stopping activé).
- **Paths** : Localisation des dossiers `train`, `val`, et `test`.

---

## 📊 Suivi des Performances

### Visualisation en Temps Réel
Suivez l'évolution de la perte (loss) et de la précision (accuracy) :
```bash
tensorboard --logdir logs/
```
Puis accédez à [http://localhost:6006](http://localhost:6006).

### Inférence & Mapping
Le système génère automatiquement `classes.json` pour garantir que les labels (Positive/Negative) sont correctement mappés entre l'entraînement et l'API d'inférence.

---

## 📦 Gestion des Modèles & Déploiement

Le modèle `.h5` est volumineux et géré via un pipeline Docker :
1. **Validation** : Le script `train.py` vérifie la précision finale.
2. **Transfert** : Utilisation de `./push_model.sh` pour synchroniser le modèle avec Docker Hub.
3. **Packaging** : Le modèle est intégré dans l'image Docker du service d'inférence pour un déploiement sécurisé.

---

<div align="center">

**🔬 Unité de Recherche ML - Système de Détection du Cancer**
© 2026 | Master 2 Informatique

</div>
