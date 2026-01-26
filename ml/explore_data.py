"""
Script d'exploration et visualisation des données
"""

import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from PIL import Image
import numpy as np
from collections import Counter
import random


def plot_class_distribution(data_dir, output_path='class_distribution.png'):
    """Visualiser la distribution des classes"""
    
    data_path = Path(data_dir)
    class_counts = {}
    
    for class_dir in data_path.iterdir():
        if not class_dir.is_dir():
            continue
        class_name = class_dir.name
        images = list(class_dir.glob('*.jpg')) + list(class_dir.glob('*.jpeg')) + list(class_dir.glob('*.png'))
        class_counts[class_name] = len(images)
    
    # Plot
    plt.figure(figsize=(10, 6))
    classes = list(class_counts.keys())
    counts = list(class_counts.values())
    
    colors = ['#FF6B6B' if c == 'Positive' else '#51CF66' for c in classes]
    
    plt.bar(classes, counts, color=colors, edgecolor='black', linewidth=1.5)
    plt.title('Distribution des Classes', fontsize=16, fontweight='bold')
    plt.xlabel('Classe', fontsize=12)
    plt.ylabel('Nombre d\'images', fontsize=12)
    
    # Ajouter les valeurs sur les barres
    for i, (class_name, count) in enumerate(zip(classes, counts)):
        plt.text(i, count + max(counts)*0.01, str(count), ha='center', fontweight='bold')
    
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✅ Distribution des classes sauvegardée: {output_path}")


def plot_sample_images(data_dir, n_samples=5, output_path='sample_images.png'):
    """Afficher des échantillons d'images de chaque classe"""
    
    data_path = Path(data_dir)
    
    classes = [d for d in data_path.iterdir() if d.is_dir()]
    n_classes = len(classes)
    
    fig, axes = plt.subplots(n_classes, n_samples, figsize=(n_samples*3, n_classes*3))
    
    if n_classes == 1:
        axes = [axes]
    
    for i, class_dir in enumerate(classes):
        class_name = class_dir.name
        images = list(class_dir.glob('*.jpg')) + list(class_dir.glob('*.jpeg')) + list(class_dir.glob('*.png'))
        
        # Sélectionner aléatoirement n_samples images
        samples = random.sample(images, min(n_samples, len(images)))
        
        for j, img_path in enumerate(samples):
            img = Image.open(img_path)
            
            ax = axes[i][j] if n_classes > 1 else axes[j]
            ax.imshow(img)
            ax.axis('off')
            
            if j == 0:
                ax.set_ylabel(class_name, fontsize=14, fontweight='bold', rotation=0, labelpad=50, va='center')
    
    plt.suptitle('Échantillons d\'Images par Classe', fontsize=16, fontweight='bold', y=0.98)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✅ Échantillons d'images sauvegardés: {output_path}")


def plot_image_size_distribution(data_dir, output_path='size_distribution.png'):
    """Visualiser la distribution des tailles d'images"""
    
    data_path = Path(data_dir)
    
    widths = []
    heights = []
    
    for class_dir in data_path.iterdir():
        if not class_dir.is_dir():
            continue
        
        for img_path in class_dir.glob('*'):
            if img_path.suffix.lower() not in ['.jpg', '.jpeg', '.png']:
                continue
            
            try:
                img = Image.open(img_path)
                w, h = img.size
                widths.append(w)
                heights.append(h)
            except:
                continue
    
    # Plot
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    # Histogramme des largeurs
    axes[0].hist(widths, bins=50, color='#0066CC', edgecolor='black', alpha=0.7)
    axes[0].set_title('Distribution des Largeurs', fontweight='bold')
    axes[0].set_xlabel('Largeur (pixels)')
    axes[0].set_ylabel('Fréquence')
    axes[0].axvline(np.mean(widths), color='red', linestyle='--', label='Moyenne', linewidth=2)
    axes[0].legend()
    
    # Histogramme des hauteurs
    axes[1].hist(heights, bins=50, color='#00C896', edgecolor='black', alpha=0.7)
    axes[1].set_title('Distribution des Hauteurs', fontweight='bold')
    axes[1].set_xlabel('Hauteur (pixels)')
    axes[1].set_ylabel('Fréquence')
    axes[1].axvline(np.mean(heights), color='red', linestyle='--', label='Moyenne', linewidth=2)
    axes[1].legend()
    
    # Scatter plot des dimensions
    axes[2].scatter(widths, heights, alpha=0.5, c='#FF6B6B', edgecolors='black', linewidth=0.5)
    axes[2].set_title('Largeur vs Hauteur', fontweight='bold')
    axes[2].set_xlabel('Largeur (pixels)')
    axes[2].set_ylabel('Hauteur (pixels)')
    axes[2].plot([0, max(widths)], [0, max(widths)], 'k--', alpha=0.3, label='Carré')
    axes[2].legend()
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✅ Distribution des tailles sauvegardée: {output_path}")
    print(f"   Largeur moyenne: {np.mean(widths):.0f}px (min: {min(widths)}, max: {max(widths)})")
    print(f"   Hauteur moyenne: {np.mean(heights):.0f}px (min: {min(heights)}, max: {max(heights)})")


def plot_pixel_intensity_distribution(data_dir, n_samples=100, output_path='intensity_distribution.png'):
    """Visualiser la distribution des intensités de pixels"""
    
    data_path = Path(data_dir)
    
    all_pixels = {class_dir.name: [] for class_dir in data_path.iterdir() if class_dir.is_dir()}
    
    for class_dir in data_path.iterdir():
        if not class_dir.is_dir():
            continue
        
        class_name = class_dir.name
        images = list(class_dir.glob('*.jpg')) + list(class_dir.glob('*.jpeg')) + list(class_dir.glob('*.png'))
        
        # Échantillonner
        samples = random.sample(images, min(n_samples, len(images)))
        
        for img_path in samples:
            try:
                img = Image.open(img_path).convert('L')  # Grayscale
                pixels = np.array(img).flatten()
                all_pixels[class_name].extend(pixels)
            except:
                continue
    
    # Plot
    plt.figure(figsize=(12, 6))
    
    for class_name, pixels in all_pixels.items():
        if pixels:
            color = '#FF6B6B' if class_name == 'Positive' else '#51CF66'
            plt.hist(pixels, bins=50, alpha=0.6, label=class_name, color=color, edgecolor='black')
    
    plt.title('Distribution des Intensités de Pixels', fontsize=16, fontweight='bold')
    plt.xlabel('Intensité (0-255)', fontsize=12)
    plt.ylabel('Fréquence', fontsize=12)
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✅ Distribution des intensités sauvegardée: {output_path}")


def explore_dataset(data_dir, output_dir='exploration'):
    """Exploration complète du dataset"""
    
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    print(f"\n🔍 Exploration du dataset: {data_dir}")
    print(f"📁 Résultats dans: {output_dir}\n")
    
    plot_class_distribution(data_dir, output_path / 'class_distribution.png')
    plot_sample_images(data_dir, output_path=output_path / 'sample_images.png')
    plot_image_size_distribution(data_dir, output_path / 'size_distribution.png')
    plot_pixel_intensity_distribution(data_dir, output_path=output_path / 'intensity_distribution.png')
    
    print(f"\n✅ Exploration terminée! Consultez {output_dir}/ pour les visualisations")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python explore_data.py <data_directory> [output_directory]")
        sys.exit(1)
    
    data_dir = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else 'exploration'
    
    explore_dataset(data_dir, output_dir)
