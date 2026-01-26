"""
Script d'entraînement du modèle CNN pour la détection du cancer du sein
"""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np
import yaml
import json
from pathlib import Path
from datetime import datetime
import argparse

def load_config(config_path="config.yaml"):
    """Charger la configuration depuis YAML"""
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def build_model(input_shape=(128, 128, 3), num_classes=1):
    """
    Construire le modèle CNN
    
    Architecture:
    - 3 blocs Conv2D + MaxPooling
    - Flatten
    - 2 couches Dense avec Dropout
    - Sortie sigmoid pour classification binaire
    """
    
    model = keras.Sequential([
        # Bloc 1
        layers.Conv2D(32, (3, 3), activation='relu', padding='same', input_shape=input_shape),
        layers.BatchNormalization(),
        layers.Conv2D(32, (3, 3), activation='relu', padding='same'),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.25),
        
        # Bloc 2
        layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
        layers.BatchNormalization(),
        layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.25),
        
        # Bloc 3
        layers.Conv2D(128, (3, 3), activation='relu', padding='same'),
        layers.BatchNormalization(),
        layers.Conv2D(128, (3, 3), activation='relu', padding='same'),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.25),
        
        # Fully Connected
        layers.Flatten(),
        layers.Dense(256, activation='relu'),
        layers.BatchNormalization(),
        layers.Dropout(0.5),
        layers.Dense(128, activation='relu'),
        layers.BatchNormalization(),
        layers.Dropout(0.5),
        layers.Dense(num_classes, activation='sigmoid')
    ])
    
    return model


def create_data_augmentation():
    """Créer le pipeline d'augmentation de données"""
    
    return keras.Sequential([
        layers.RandomFlip("horizontal"),
        layers.RandomRotation(0.2),
        layers.RandomZoom(0.2),
        layers.RandomContrast(0.2),
    ])


def load_datasets(config):
    """Charger les datasets d'entraînement et de validation"""
    
    img_height = config['model']['img_height']
    img_width = config['model']['img_width']
    batch_size = config['training']['batch_size']
    
    # Training dataset
    train_ds = keras.preprocessing.image_dataset_from_directory(
        config['data']['train_dir'],
        image_size=(img_height, img_width),
        batch_size=batch_size,
        label_mode='binary'
    )
    
    # Validation dataset
    val_ds = keras.preprocessing.image_dataset_from_directory(
        config['data']['val_dir'],
        image_size=(img_height, img_width),
        batch_size=batch_size,
        label_mode='binary'
    )
    
    # Normalize to [0, 1]
    normalization_layer = layers.Rescaling(1./255)
    train_ds = train_ds.map(lambda x, y: (normalization_layer(x), y))
    val_ds = val_ds.map(lambda x, y: (normalization_layer(x), y))
    
    # Performance optimization
    AUTOTUNE = tf.data.AUTOTUNE
    train_ds = train_ds.cache().prefetch(buffer_size=AUTOTUNE)
    val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)
    
    return train_ds, val_ds


def train_model(config, model, train_ds, val_ds):
    """Entraîner le modèle"""
    
    # Compile model
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=config['training']['learning_rate']),
        loss='binary_crossentropy',
        metrics=[
            'accuracy',
            keras.metrics.AUC(name='auc'),
            keras.metrics.Precision(name='precision'),
            keras.metrics.Recall(name='recall')
        ]
    )
    
    # Create checkpoint directory
    checkpoint_dir = Path(config['model']['checkpoint_dir'])
    checkpoint_dir.mkdir(parents=True, exist_ok=True)
    
    # Callbacks
    callbacks = [
        keras.callbacks.ModelCheckpoint(
            filepath=str(checkpoint_dir / 'model_epoch_{epoch:02d}_acc_{val_accuracy:.4f}.h5'),
            save_best_only=True,
            monitor='val_accuracy',
            mode='max',
            verbose=1
        ),
        keras.callbacks.EarlyStopping(
            monitor='val_loss',
            patience=config['training']['early_stopping_patience'],
            restore_best_weights=True,
            verbose=1
        ),
        keras.callbacks.ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=5,
            min_lr=1e-7,
            verbose=1
        ),
        keras.callbacks.TensorBoard(
            log_dir=f"logs/{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            histogram_freq=1
        )
    ]
    
    # Train
    print("\n🚀 Starting training...")
    print(f"Epochs: {config['training']['epochs']}")
    print(f"Batch size: {config['training']['batch_size']}")
    print(f"Learning rate: {config['training']['learning_rate']}\n")
    
    history = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=config['training']['epochs'],
        callbacks=callbacks,
        verbose=1
    )
    
    return history


def save_model_and_metrics(model, history, config):
    """Sauvegarder le modèle et les métriques"""
    
    # Save final model
    output_path = Path(config['model']['output_path'])
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    model.save(str(output_path))
    print(f"\n✅ Modèle sauvegardé: {output_path}")
    
    # Save training history
    history_path = output_path.parent / 'training_history.json'
    history_dict = {key: [float(val) for val in values] for key, values in history.history.items()}
    
    with open(history_path, 'w') as f:
        json.dump(history_dict, f, indent=2)
    
    print(f"✅ Historique sauvegardé: {history_path}")
    
    # Save metrics summary
    metrics_summary = {
        'final_accuracy': float(history.history['accuracy'][-1]),
        'final_val_accuracy': float(history.history['val_accuracy'][-1]),
        'final_loss': float(history.history['loss'][-1]),
        'final_val_loss': float(history.history['val_loss'][-1]),
        'final_auc': float(history.history['auc'][-1]),
        'final_val_auc': float(history.history['val_auc'][-1]),
        'best_val_accuracy': float(max(history.history['val_accuracy'])),
        'epochs_trained': len(history.history['accuracy']),
        'timestamp': datetime.now().isoformat()
    }
    
    metrics_path = output_path.parent / 'metrics.json'
    with open(metrics_path, 'w') as f:
        json.dump(metrics_summary, f, indent=2)
    
    print(f"✅ Métriques sauvegardées: {metrics_path}")
    
    # Print summary
    print("\n📊 Training Summary:")
    print(f"Final Training Accuracy: {metrics_summary['final_accuracy']:.4f}")
    print(f"Final Validation Accuracy: {metrics_summary['final_val_accuracy']:.4f}")
    print(f"Best Validation Accuracy: {metrics_summary['best_val_accuracy']:.4f}")
    print(f"Final AUC: {metrics_summary['final_auc']:.4f}")
    
    return metrics_summary


def main():
    parser = argparse.ArgumentParser(description='Train cancer detection model')
    parser.add_argument('--config', type=str, default='config.yaml', help='Path to config file')
    args = parser.parse_args()
    
    # Load config
    config = load_config(args.config)
    
    print("=" * 60)
    print("🏥 Cancer Detection Model Training")
    print("=" * 60)
    
    # Load datasets
    print("\n📂 Loading datasets...")
    train_ds, val_ds = load_datasets(config)
    
    # Build model
    print("\n🏗️  Building model...")
    input_shape = (
        config['model']['img_height'],
        config['model']['img_width'],
        config['model']['channels']
    )
    model = build_model(input_shape=input_shape)
    
    # Print model summary
    print("\n📋 Model Summary:")
    model.summary()
    
    # Train model
    history = train_model(config, model, train_ds, val_ds)
    
    # Save model and metrics
    metrics_summary = save_model_and_metrics(model, history, config)
    
    print("\n" + "=" * 60)
    print("✅ Training completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
