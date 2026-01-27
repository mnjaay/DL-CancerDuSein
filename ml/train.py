import os
import argparse
import yaml
from model_factory import create_model
from preprocessing import create_generators
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau

def train(config_path):
    # Charger la configuration
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    # Paramètres de la configuration
    IMG_HEIGHT = config['model']['img_height']
    IMG_WIDTH = config['model']['img_width']
    BATCH_SIZE = config['training']['batch_size']
    EPOCHS = config['training']['epochs']
    
    # Utiliser des chemins explicites de la configuration
    TRAIN_DIR = config['data']['train_dir']
    VAL_DIR = config['data']['val_dir']
    TEST_DIR = config['data']['test_dir']
    
    OUTPUT_PATH = config['model']['output_path']
    PATIENCE = config['training']['early_stopping_patience']

    # 1. Créer les générateurs
    train_generator, validation_generator, test_generator = create_generators(
        TRAIN_DIR, VAL_DIR, TEST_DIR, IMG_HEIGHT, IMG_WIDTH, BATCH_SIZE
    )

    # 2. Créer le modèle
    model = create_model(input_shape=(IMG_HEIGHT, IMG_WIDTH, 3))
    
    # 3. Callbacks (Rappels)
    early_stopping = EarlyStopping(monitor='val_loss', patience=PATIENCE, restore_best_weights=True)
    lr_scheduler = ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=2, verbose=1, min_lr=1e-6)

    # 4. Entraînement
    print(f"Début de l'entraînement pour {EPOCHS} époques...")
    history = model.fit(
        train_generator,
        epochs=EPOCHS,
        validation_data=validation_generator,
        verbose=1,
        callbacks=[early_stopping, lr_scheduler]
    )

    # 5. Évaluer
    print("Évaluation sur l'ensemble de test...")
    loss, accuracy = model.evaluate(test_generator)
    print(f"Perte de test (Loss): {loss:.4f}")
    print(f"Précision de test (Accuracy): {accuracy:.4f}")

    # 6. Sauvegarder le modèle
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    model.save(OUTPUT_PATH)
    print(f"Modèle sauvegardé dans {OUTPUT_PATH}")
    
    # Sauvegarder également une copie dans ml/ pour référence
    model.save("model.h5")
    print("Modèle de référence sauvegardé dans ml/model.h5")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, default="ml/config.yaml", help="Chemin vers config.yaml")
    args = parser.parse_args()

    # Déterminer le chemin correct pour la configuration
    config_file = args.config
    if not os.path.exists(config_file):
        if os.path.exists("config.yaml"):
            config_file = "config.yaml"
        elif os.path.exists("ml/config.yaml"):
            config_file = "ml/config.yaml"

    train(config_file)
