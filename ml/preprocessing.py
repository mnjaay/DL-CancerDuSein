import tensorflow as tf
import os
import argparse
import shutil
from sklearn.model_selection import train_test_split
from tqdm import tqdm

def create_generators(train_dir, val_dir, test_dir, img_height=128, img_width=128, batch_size=32):
    """
    Crée des ImageDataGenerators pour l'entraînement, la validation et les tests en utilisant des chemins explicites.
    """
    # Augmentation des données pour l'entraînement
    train_datagen = tf.keras.preprocessing.image.ImageDataGenerator(
        rescale=1./255,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        vertical_flip=True,
        fill_mode='nearest'
    )

    # Uniquement redimensionnement pour la validation et les tests
    val_test_datagen = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1./255)

    print(f"Chargement des données d'entraînement depuis {train_dir}...")
    train_generator = train_datagen.flow_from_directory(
        train_dir,
        target_size=(img_height, img_width),
        batch_size=batch_size,
        class_mode='binary',
        color_mode='rgb',
        shuffle=True,
        seed=123
    )

    print(f"Chargement des données de validation depuis {val_dir}...")
    validation_generator = val_test_datagen.flow_from_directory(
        val_dir,
        target_size=(img_height, img_width),
        batch_size=batch_size,
        class_mode='binary',
        color_mode='rgb',
        shuffle=False,
        seed=123
    )

    print(f"Chargement des données de test depuis {test_dir}...")
    test_generator = val_test_datagen.flow_from_directory(
        test_dir,
        target_size=(img_height, img_width),
        batch_size=batch_size,
        class_mode='binary',
        color_mode='rgb',
        shuffle=False,
        seed=123
    )

    return train_generator, validation_generator, test_generator

def prepare_data(input_dir, output_dir, img_size=128, split_ratio=(0.7, 0.15, 0.15)):
    """
    Divise les images brutes en répertoires train, val et test.
    """
    print(f"Préparation des données de {input_dir} vers {output_dir}...")
    
    classes = [d for d in os.listdir(input_dir) if os.path.isdir(os.path.join(input_dir, d))]
    
    for cls in classes:
        cls_dir = os.path.join(input_dir, cls)
        images = [f for f in os.listdir(cls_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        
        # Diviser les images
        train_imgs, temp_imgs = train_test_split(images, test_size=(1 - split_ratio[0]), random_state=42)
        val_imgs, test_imgs = train_test_split(temp_imgs, test_size=(split_ratio[2] / (split_ratio[1] + split_ratio[2])), random_state=42)
        
        for split, split_imgs in zip(['train', 'val', 'test'], [train_imgs, val_imgs, test_imgs]):
            split_cls_dir = os.path.join(output_dir, split, cls)
            os.makedirs(split_cls_dir, exist_ok=True)
            
            print(f"Copie de {len(split_imgs)} images vers {split_cls_dir}...")
            for img in tqdm(split_imgs, desc=f"{split}/{cls}"):
                shutil.copy2(os.path.join(cls_dir, img), os.path.join(split_cls_dir, img))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")
    
    # Commande de préparation (Prepare)
    prepare_parser = subparsers.add_parser("prepare")
    prepare_parser.add_argument("--input", type=str, required=True, help="Répertoire des données brutes")
    prepare_parser.add_argument("--output", type=str, required=True, help="Répertoire de sortie pour les divisions")
    prepare_parser.add_argument("--size", type=int, default=128, help="Taille de l'image (conservé pour compatibilité)")
    
    args = parser.parse_args()
    
    if args.command == "prepare":
        prepare_data(args.input, args.output, args.size)
    else:
        parser.print_help()
