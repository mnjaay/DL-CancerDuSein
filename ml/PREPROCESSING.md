# 🧹 Guide de Preprocessing des Données

## Scripts Disponibles

### 1. preprocessing.py - Nettoyage et Préparation

#### Analyser votre dataset

```bash
python preprocessing.py analyze --input data/raw

# Output: Rapport détaillé avec:
# - Nombre d'images total
# - Images valides vs invalides
# - Distribution par classe
# - Erreurs détectées
# - Rapport saved as JSON
```

#### Nettoyer le dataset

```bash
python preprocessing.py clean \
  --input data/raw \
  --output data/cleaned \
  --size 128 \
  --mode RGB

# Actions effectuées:
# ✅ Validation de chaque image
# ✅ Conversion au format RGB
# ✅ Resize à 128x128
# ✅ Sauvegarde en JPEG qualité 95%
# ✅ Suppression des images invalides
```

Options:
- `--size`: Taille cible (défaut: 128)
- `--mode`: RGB ou L (grayscale)
- `--keep-invalid`: Garder les images invalides

#### Équilibrer les classes

```bash
# Undersample (réduire à la classe minoritaire)
python preprocessing.py balance \
  --input data/cleaned \
  --strategy undersample

# Oversample (augmenter par duplication)
python preprocessing.py balance \
  --input data/cleaned \
  --strategy oversample

# Target spécifique
python preprocessing.py balance \
  --input data/cleaned \
  --target-count 1000
```

---

### 2. explore_data.py - Exploration Visuelle

```bash
python explore_data.py data/cleaned exploration_results
```

**Génère 4 visualisations** :

1. **class_distribution.png** - Distribution des classes
2. **sample_images.png** - Échantillons d'images (5 par classe)
3. **size_distribution.png** - Distribution des tailles (largeur, hauteur, scatter)
4. **intensity_distribution.png** - Distribution des intensités de pixels

---

## Workflow Complet de Preprocessing

### Étape 1 : Organisation Initiale

```bash
# Créer la structure
mkdir -p data/raw/{Positive,Negative}

# Copier vos images brutes
cp /path/to/positive_images/* data/raw/Positive/
cp /path/to/negative_images/* data/raw/Negative/
```

### Étape 2 : Analyse

```bash
# Analyser pour détecter les problèmes
python preprocessing.py analyze --input data/raw

# Examiner le rapport
cat analysis_report_raw.json
```

**Problèmes courants détectés** :
- Images corrompues
- Formats non supportés
- Tailles trop petites/grandes
- Fichiers invalides

### Étape 3 : Nettoyage

```bash
# Nettoyer et normaliser
python preprocessing.py clean \
  --input data/raw \
  --output data/cleaned \
  --size 128 \
  --mode RGB

# Résultat:
# data/cleaned/
# ├── Positive/  (toutes 128x128 RGB JPEG)
# └── Negative/  (toutes 128x128 RGB JPEG)
```

### Étape 4 : Exploration

```bash
# Générer les visualisations
python explore_data.py data/cleaned exploration

# Examiner les graphiques
open exploration/class_distribution.png
open exploration/sample_images.png
```

### Étape 5 : Équilibrage (si nécessaire)

```bash
# Vérifier la distribution
# Si déséquilibre, équilibrer

python preprocessing.py balance \
  --input data/cleaned \
  --strategy undersample  # ou oversample
```

### Étape 6 : Split Train/Val/Test

```bash
# Créer un script de split (ou manuel)
python -c "
import shutil
from pathlib import Path
import random

def split_dataset(source, dest, split=(0.7, 0.15, 0.15)):
    '''Split en train/val/test'''
    source_path = Path(source)
    dest_path = Path(dest)
    
    for class_dir in source_path.iterdir():
        if not class_dir.is_dir():
            continue
        
        class_name = class_dir.name
        images = list(class_dir.glob('*.jpg'))
        random.shuffle(images)
        
        n_train = int(len(images) * split[0])
        n_val = int(len(images) * split[1])
        
        train_images = images[:n_train]
        val_images = images[n_train:n_train+n_val]
        test_images = images[n_train+n_val:]
        
        # Créer les dossiers
        for subset in ['train', 'val', 'test']:
            (dest_path / subset / class_name).mkdir(parents=True, exist_ok=True)
        
        # Copier
        for img in train_images:
            shutil.copy2(img, dest_path / 'train' / class_name / img.name)
        for img in val_images:
            shutil.copy2(img, dest_path / 'val' / class_name / img.name)
        for img in test_images:
            shutil.copy2(img, dest_path / 'test' / class_name / img.name)
    
    print('✅ Split terminé!')

split_dataset('data/cleaned', 'data')
"
```

### Étape 7 : Vérification Finale

```bash
# Analyser chaque subset
python preprocessing.py analyze --input data/train
python preprocessing.py analyze --input data/val
python preprocessing.py analyze --input data/test

# Explorer visuellement
python explore_data.py data/train exploration_train
python explore_data.py data/val exploration_val
python explore_data.py data/test exploration_test
```

---

## Checklist Complète

- [ ] Données brutes copiées dans `data/raw/`
- [ ] Analyse effectuée (`analyze`)
- [ ] Données nettoyées (`clean`)
- [ ] Exploration visuelle générée
- [ ] Classes équilibrées si nécessaire
- [ ] Split train/val/test effectué (70/15/15)
- [ ] Vérification finale de chaque subset
- [ ] Prêt pour l'entraînement ! 🚀

---

## Exemples de Sortie

### Analyse

```
📊 Résultats de l'analyse:
  Total d'images: 2000
  Images valides: 1950
  Images invalides: 50

📂 Distribution par classe:
  - Positive:
      Total: 1000
      Valides: 975
      Invalides: 25
  - Negative:
      Total: 1000
      Valides: 975
      Invalides: 25

❌ Erreurs (10 premières):
  - img_123.jpg: Image trop petite: 32x32
  - img_456.jpg: Mode non supporté: CMYK
  ...
```

### Nettoyage

```
🧹 Nettoyage du dataset: data/raw
📁 Destination: data/cleaned
🎯 Taille cible: (128, 128)
🎨 Mode cible: RGB

📂 Traitement de la classe: Positive
  Positive: 100%|████████| 1000/1000
📂 Traitement de la classe: Negative
  Negative: 100%|████████| 1000/1000

✅ Nettoyage terminé!
📊 Statistiques:
  - Images traitées: 2000
  - Images valides: 1950
  - Images nettoyées: 1950
  - Images invalides: 50
```

### Équilibrage

```
⚖️ Équilibrage du dataset
Distribution actuelle:
  - Positive: 1200 images
  - Negative: 800 images

🎯 Objectif: 800 images par classe
📐 Stratégie: undersample

📉 Positive: 1200 → 800 (supprimé 400)
✅ Negative: Déjà équilibré (800)

✅ Équilibrage terminé!
```

---

## Conseils

### Qualité des Données

- ✅ Résolution minimale : 50x50
- ✅ Format : JPEG, PNG
- ✅ Mode : RGB de préférence
- ✅ Taille fichier : 1KB - 50MB

### Équilibrage

- **Undersample** : Si beaucoup de données
- **Oversample** : Si peu de données (risque d'overfitting)
- **SMOTE** : Pour générer de vraies nouvelles images (avancé)

### Split

- **70/15/15** : Standard
- **80/10/10** : Si beaucoup de données
- **60/20/20** : Si peu de données

---

Prêt à nettoyer vos données ! 🧹✨
