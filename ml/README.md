# 🤖 Guide d'Entraînement Deep Learning

Ce dossier contient l'expertise et les outils nécessaires pour préparer les données, entraîner le modèle de vision par ordinateur et valider ses performances.

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
Structure requise pour le chargement dynamique des classes :
```text
ml/data/raw/
├── Positive/  (Images de mammographies avec signes cliniques)
└── Negative/  (Images de mammographies saines)
```

### 3. Prétraitement & Nettoyage
Normalisation des images (128x128), équilibrage des classes et suppression des artéfacts :
```bash
python preprocessing.py clean --input data/raw --output data/cleaned
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
- **Paths** : Localisation des dossiers de données.

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

Contrairement aux fichiers sources légers, le modèle `.h5` est volumineux. Le flux de travail privilégié est :
1. **Validation** : Le script `train.py` vérifie la précision minimale requise.
2. **Transfert** : Utilisation du script `./push_model.sh` pour synchroniser le modèle avec l'environnement de production.
3. **Packaging** : Le modèle est intégré directement dans l'image Docker du service d'inférence pour garantir un fonctionnement "plug-and-play" sans dépendances externes.

---

## 💡 Conseils de Recherche

1. **Équilibrage** : Toujours utiliser le script `preprocessing.py` pour éviter le biais vers une classe spécifique (Data Balancing).
2. **Régularisation** : Un Dropout de 0.5 est appliqué aux couches denses pour prévenir l'overfitting.
3. **Augmentation** : L'augmentation de données en temps réel (rotations, flips) est intégrée par défaut dans les générateurs.

---

<div align="center">

**🔬 Unité de Recherche ML - Système de Détection du Cancer**
© 2026 | Master 2 Informatique

</div>
