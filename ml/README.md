# 🤖 Guide d'Entraînement Deep Learning

Ce dossier contient tous les outils nécessaires pour préparer les données, entraîner le modèle CNN et évaluer ses performances.

---

## 🚀 Démarrage Rapide

### 1. Préparer l'Environnement
Nous recommandons d'utiliser le script de setup à la racine du projet :
```bash
cd ..
./setup_ml.sh
source ml/venv/bin/activate
cd ml
```

### 2. Organisation des Données
Placez vos images brutes dans la structure suivante :
```text
ml/data/raw/
├── Positive/  (Images avec cancer)
└── Negative/  (Images saines)
```

### 3. Nettoyer et Préparer (Preprocessing)
Lancer le script de nettoyage pour normaliser les images (128x128) et équilibrer les classes :
```bash
python preprocessing.py clean --input data/raw --output data/cleaned
```

### 4. Entraîner le Modèle
```bash
python train.py --config config.yaml
```
*Le modèle sera automatiquement sauvegardé dans `../inference-service/models/model.h5`.*

---

## ⚙️ Configuration (`config.yaml`)

Vous pouvez personnaliser l'entraînement sans toucher au code :
- **Data**: Chemins vers les dossiers `train`, `val`, `test`.
- **Model**: Taille des images (par défaut 128x128), architecture.
- **Training**: Batch size, nombre d'époques, taux d'apprentissage (learning rate).
- **Callbacks**: Early stopping et réduction de LR sur plateau.

---

## 📊 Évaluation et Visualisation

### Rapports de Performance
Après l'entraînement, générez un rapport complet :
```bash
python evaluate.py ../inference-service/models/model.h5 data/cleaned/test
```
Ce script génère :
- Une **Matrice de Confusion**.
- Les courbes **ROC** et **Precision-Recall**.
- Un fichier `metrics.json` pour le suivi.

### TensorBoard
Pour suivre l'entraînement en temps réel :
```bash
tensorboard --logdir logs/
```
Puis ouvrez [http://localhost:6006](http://localhost:6006).

---

## 🐘 Gestion des Modèles Lourds (Git LFS)

Les fichiers `.h5` sont gérés par **Git LFS** pour ne pas alourdir le dépôt.
1. Assurez-vous que LFS est installé (`brew install git-lfs`).
2. Lors d'un `push`, le modèle est envoyé sur les serveurs de stockage d'objets de GitHub.
3. Le workflow GitHub Actions détecte le changement et lance le déploiement.

---

## 💡 Conseils pour l'Entraînement

1. **Équilibre des classes**: Le script `preprocessing.py` gère l'undersampling/oversampling. Utilisez-le pour éviter que le modèle ne favorise une classe.
2. **Transfer Learning**: Si vos résultats stagnent, envisagez de modifier `train.py` pour utiliser une base **VGG16** ou **ResNet50** pré-entraînée sur ImageNet.
3. **Dropout**: Une valeur de 0.5 est utilisée par défaut pour limiter l'overfitting sur les petits datasets.

---

<div align="center">

**🔬 ML Research Unit - Cancer Detection System**
© 2025 | Happy Training!

</div>
