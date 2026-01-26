"""
Script de preprocessing et nettoyage des données
"""

import os
import shutil
from pathlib import Path
from PIL import Image
import numpy as np
from tqdm import tqdm
import argparse
import json


def validate_image(image_path):
    """
    Valider qu'une image est correcte
    
    Returns:
        tuple: (is_valid, error_message, image_info)
    """
    try:
        # Ouvrir l'image
        img = Image.open(image_path)
        
        # Vérifier le mode
        if img.mode not in ['RGB', 'L', 'RGBA']:
            return False, f"Mode non supporté: {img.mode}", None
        
        # Vérifier les dimensions
        width, height = img.size
        if width < 50 or height < 50:
            return False, f"Image trop petite: {width}x{height}", None
        
        # Vérifier que l'image peut être chargée complètement
        img.load()
        
        # Vérifier la taille du fichier
        file_size = os.path.getsize(image_path)
        if file_size < 1024:  # Moins de 1KB
            return False, f"Fichier trop petit: {file_size} bytes", None
        
        if file_size > 50 * 1024 * 1024:  # Plus de 50MB
            return False, f"Fichier trop gros: {file_size / (1024*1024):.1f} MB", None
        
        info = {
            'size': (width, height),
            'mode': img.mode,
            'format': img.format,
            'file_size': file_size
        }
        
        return True, None, info
        
    except Exception as e:
        return False, f"Erreur lors de l'ouverture: {str(e)}", None


def clean_image(image_path, target_size=(128, 128), target_mode='RGB'):
    """
    Nettoyer et normaliser une image
    
    Args:
        image_path: Chemin vers l'image
        target_size: Taille cible (width, height)
        target_mode: Mode cible (RGB, L)
    
    Returns:
        PIL.Image: Image nettoyée
    """
    img = Image.open(image_path)
    
    # Convertir au mode cible
    if img.mode != target_mode:
        if target_mode == 'RGB' and img.mode == 'RGBA':
            # Créer un fond blanc pour les images avec transparence
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[3])  # Alpha channel
            img = background
        else:
            img = img.convert(target_mode)
    
    # Resize
    img = img.resize(target_size, Image.Resampling.LANCZOS)
    
    return img


def analyze_dataset(data_dir):
    """
    Analyser un dataset et retourner des statistiques
    
    Returns:
        dict: Statistiques du dataset
    """
    data_path = Path(data_dir)
    
    stats = {
        'total_images': 0,
        'classes': {},
        'valid_images': 0,
        'invalid_images': 0,
        'errors': [],
        'size_distribution': [],
        'mode_distribution': {},
        'format_distribution': {}
    }
    
    # Parcourir les classes
    for class_dir in data_path.iterdir():
        if not class_dir.is_dir():
            continue
        
        class_name = class_dir.name
        stats['classes'][class_name] = {
            'count': 0,
            'valid': 0,
            'invalid': 0
        }
        
        # Parcourir les images
        for img_path in class_dir.glob('*'):
            if img_path.suffix.lower() not in ['.jpg', '.jpeg', '.png', '.bmp']:
                continue
            
            stats['total_images'] += 1
            stats['classes'][class_name]['count'] += 1
            
            # Valider l'image
            is_valid, error, info = validate_image(img_path)
            
            if is_valid:
                stats['valid_images'] += 1
                stats['classes'][class_name]['valid'] += 1
                
                # Statistiques supplémentaires
                stats['size_distribution'].append(info['size'])
                stats['mode_distribution'][info['mode']] = stats['mode_distribution'].get(info['mode'], 0) + 1
                if info['format']:
                    stats['format_distribution'][info['format']] = stats['format_distribution'].get(info['format'], 0) + 1
            else:
                stats['invalid_images'] += 1
                stats['classes'][class_name]['invalid'] += 1
                stats['errors'].append({
                    'file': str(img_path),
                    'error': error
                })
    
    return stats


def clean_dataset(input_dir, output_dir, target_size=(128, 128), target_mode='RGB', remove_invalid=True):
    """
    Nettoyer un dataset complet
    
    Args:
        input_dir: Dossier source
        output_dir: Dossier destination
        target_size: Taille cible des images
        target_mode: Mode couleur cible
        remove_invalid: Supprimer les images invalides
    """
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    
    # Créer le dossier de sortie
    output_path.mkdir(parents=True, exist_ok=True)
    
    print(f"\n🧹 Nettoyage du dataset: {input_dir}")
    print(f"📁 Destination: {output_dir}")
    print(f"🎯 Taille cible: {target_size}")
    print(f"🎨 Mode cible: {target_mode}\n")
    
    stats = {
        'processed': 0,
        'valid': 0,
        'invalid': 0,
        'cleaned': 0
    }
    
    # Parcourir les classes
    for class_dir in input_path.iterdir():
        if not class_dir.is_dir():
            continue
        
        class_name = class_dir.name
        print(f"📂 Traitement de la classe: {class_name}")
        
        # Créer le dossier de classe de sortie
        output_class_dir = output_path / class_name
        output_class_dir.mkdir(parents=True, exist_ok=True)
        
        # Parcourir les images
        images = list(class_dir.glob('*'))
        images = [img for img in images if img.suffix.lower() in ['.jpg', '.jpeg', '.png', '.bmp']]
        
        for img_path in tqdm(images, desc=f"  {class_name}"):
            stats['processed'] += 1
            
            # Valider
            is_valid, error, info = validate_image(img_path)
            
            if is_valid:
                stats['valid'] += 1
                
                try:
                    # Nettoyer l'image
                    cleaned_img = clean_image(img_path, target_size, target_mode)
                    
                    # Sauvegarder
                    output_path_img = output_class_dir / f"{img_path.stem}.jpg"
                    cleaned_img.save(output_path_img, 'JPEG', quality=95)
                    
                    stats['cleaned'] += 1
                    
                except Exception as e:
                    print(f"  ⚠️ Erreur lors du nettoyage de {img_path.name}: {e}")
                    stats['invalid'] += 1
            else:
                stats['invalid'] += 1
                if not remove_invalid:
                    # Copier quand même
                    shutil.copy2(img_path, output_class_dir / img_path.name)
                else:
                    print(f"  ❌ Image invalide ignorée: {img_path.name} - {error}")
    
    print(f"\n✅ Nettoyage terminé!")
    print(f"📊 Statistiques:")
    print(f"  - Images traitées: {stats['processed']}")
    print(f"  - Images valides: {stats['valid']}")
    print(f"  - Images nettoyées: {stats['cleaned']}")
    print(f"  - Images invalides: {stats['invalid']}")
    
    return stats


def balance_dataset(data_dir, target_count=None, strategy='undersample'):
    """
    Équilibrer les classes d'un dataset
    
    Args:
        data_dir: Dossier du dataset
        target_count: Nombre cible d'images par classe (None = min ou max selon stratégie)
        strategy: 'undersample' (réduire) ou 'oversample' (augmenter avec copies)
    """
    data_path = Path(data_dir)
    
    # Compter les images par classe
    class_counts = {}
    for class_dir in data_path.iterdir():
        if not class_dir.is_dir():
            continue
        class_name = class_dir.name
        images = list(class_dir.glob('*.jpg')) + list(class_dir.glob('*.jpeg')) + list(class_dir.glob('*.png'))
        class_counts[class_name] = len(images)
    
    print(f"\n⚖️ Équilibrage du dataset")
    print(f"Distribution actuelle:")
    for class_name, count in class_counts.items():
        print(f"  - {class_name}: {count} images")
    
    # Déterminer le target_count
    if target_count is None:
        if strategy == 'undersample':
            target_count = min(class_counts.values())
        else:  # oversample
            target_count = max(class_counts.values())
    
    print(f"\n🎯 Objectif: {target_count} images par classe")
    print(f"📐 Stratégie: {strategy}\n")
    
    # Équilibrer chaque classe
    for class_dir in data_path.iterdir():
        if not class_dir.is_dir():
            continue
        
        class_name = class_dir.name
        images = list(class_dir.glob('*.jpg')) + list(class_dir.glob('*.jpeg')) + list(class_dir.glob('*.png'))
        current_count = len(images)
        
        if current_count == target_count:
            print(f"✅ {class_name}: Déjà équilibré ({current_count})")
            continue
        
        if current_count > target_count:
            # Undersample: supprimer aléatoirement
            import random
            random.shuffle(images)
            to_remove = images[target_count:]
            
            for img in to_remove:
                img.unlink()
            
            print(f"📉 {class_name}: {current_count} → {target_count} (supprimé {len(to_remove)})")
        
        else:
            # Oversample: dupliquer aléatoirement
            import random
            needed = target_count - current_count
            to_duplicate = random.choices(images, k=needed)
            
            for i, img in enumerate(to_duplicate):
                new_name = f"{img.stem}_dup{i}{img.suffix}"
                shutil.copy2(img, img.parent / new_name)
            
            print(f"📈 {class_name}: {current_count} → {target_count} (dupliqué {needed})")
    
    print(f"\n✅ Équilibrage terminé!")


def prepare_pipeline(input_dir, output_dir, target_size=(128, 128), target_mode='RGB', split_ratios=(0.7, 0.15, 0.15)):
    """
    Pipeline complet: Nettoyage + Split (Train, Val, Test)
    """
    import random
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    
    # Prerequis: Les dossiers de sortie
    for split in ['train', 'val', 'test']:
        for cls in ['Positive', 'Negative']:
            (output_path / split / cls).mkdir(parents=True, exist_ok=True)

    print(f"\n🚀 Préparation du pipeline complet: {input_dir} -> {output_dir}")
    
    for class_name in ['Positive', 'Negative']:
        class_dir = input_path / class_name
        if not class_dir.exists():
            print(f"⚠️  Classe {class_name} non trouvée dans {input_dir}")
            continue
            
        images = list(class_dir.glob('*'))
        images = [img for img in images if img.suffix.lower() in ['.jpg', '.jpeg', '.png', '.bmp']]
        random.shuffle(images)
        
        n = len(images)
        n_train = int(n * split_ratios[0])
        n_val = int(n * split_ratios[1])
        
        splits = {
            'train': images[:n_train],
            'val': images[n_train:n_train + n_val],
            'test': images[n_train + n_val:]
        }
        
        for split_name, split_images in splits.items():
            print(f"📦 Traitement de {split_name}/{class_name} ({len(split_images)} images)...")
            count = 0
            for img_path in tqdm(split_images, desc=f"  {split_name}"):
                try:
                    is_valid, _, _ = validate_image(img_path)
                    if is_valid:
                        cleaned_img = clean_image(img_path, target_size, target_mode)
                        save_path = output_path / split_name / class_name / f"{img_path.stem}.jpg"
                        cleaned_img.save(save_path, 'JPEG', quality=95)
                        count += 1
                except Exception as e:
                    pass
            print(f"✅ Terminé: {count} images enregistrées dans {split_name}/{class_name}")

    print("\n✨ Pipeline de préparation terminé avec succès !")


def main():
    parser = argparse.ArgumentParser(description='Preprocessing et nettoyage des données')
    parser.add_argument('command', choices=['analyze', 'clean', 'balance', 'prepare'], help='Commande à exécuter')
    parser.add_argument('--input', type=str, required=True, help='Dossier d\'entrée')
    parser.add_argument('--output', type=str, help='Dossier de sortie')
    parser.add_argument('--size', type=int, default=128, help='Taille des images')
    parser.add_argument('--mode', type=str, default='RGB', choices=['RGB', 'L'], help='Mode couleur')
    parser.add_argument('--keep-invalid', action='store_true', help='Garder les images invalides')
    parser.add_argument('--strategy', type=str, default='undersample', choices=['undersample', 'oversample'], help='Stratégie d\'équilibrage')
    parser.add_argument('--target-count', type=int, help='Nombre cible d\'images par classe')
    
    args = parser.parse_args()
    
    if args.command == 'analyze':
        print("🔍 Analyse du dataset...")
        stats = analyze_dataset(args.input)
        # (rest of analyze logic kept as is...)
        print(f"\n📊 Résultats de l'analyse: Total={stats['total_images']}, Valides={stats['valid_images']}")
    
    elif args.command == 'clean':
        if not args.output:
            print("❌ --output est requis pour la commande 'clean'")
            return
        clean_dataset(args.input, args.output, target_size=(args.size, args.size), 
                      target_mode=args.mode, remove_invalid=not args.keep_invalid)
    
    elif args.command == 'prepare':
        if not args.output:
            print("❌ --output est requis pour la commande 'prepare'")
            return
        prepare_pipeline(args.input, args.output, target_size=(args.size, args.size), target_mode=args.mode)

    elif args.command == 'balance':
        balance_dataset(args.input, target_count=args.target_count, strategy=args.strategy)


if __name__ == "__main__":
    main()
