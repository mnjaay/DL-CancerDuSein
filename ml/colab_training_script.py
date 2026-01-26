# -*- coding: utf-8 -*-
"""
Colab-Ready Training Script (Transfer Learning VGG16)
Breast Cancer Detection System

Features:
- Automated Preprocessing (Clean & Split)
- Transfer Learning with VGG16
- Two-phase training: Warmup + Fine-Tuning
- Evaluaton metrics & model export
"""

import os
import shutil
import random
import json
from pathlib import Path
from datetime import datetime
from PIL import Image
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from sklearn.metrics import classification_report, confusion_matrix

# --- CONFIG ---
CONFIG = {
    'img_size': 128,
    'batch_size': 32,
    'epochs_warmup': 20,
    'epochs_fine_tune': 10,
    'lr': 0.001
}

def setup_data(input_dir='data/raw', output_dir='data/cleaned'):
    out_p = Path(output_dir)
    for s in ['train', 'val', 'test']:
        for c in ['Positive', 'Negative']: (out_p/s/c).mkdir(parents=True, exist_ok=True)
    
    in_p = Path(input_dir)
    for c in ['Positive', 'Negative']:
        imgs = list((in_p/c).glob('*'))
        random.shuffle(imgs)
        # Split 70/15/15
        n = len(imgs); n1 = int(n*0.7); n2 = int(n*0.85)
        splits = {'train': imgs[:n1], 'val': imgs[n1:n2], 'test': imgs[n2:]}
        for split, split_imgs in splits.items():
            for im_p in split_imgs:
                try:
                    with Image.open(im_p) as img:
                        img.convert("RGB").resize((128,128)).save(out_p/split/c/f"{im_p.stem}.jpg")
                except: pass
    print("✅ Données préparées.")

def run():
    # 1. Setup
    setup_data()
    
    # 2. Datasets
    get_ds = lambda p: keras.preprocessing.image_dataset_from_directory(
        p, image_size=(128,128), batch_size=32, label_mode='binary'
    ).map(lambda x,y: (layers.Rescaling(1./255)(x), y)).cache().prefetch(tf.data.AUTOTUNE)
    
    train_ds = get_ds('data/cleaned/train')
    val_ds = get_ds('data/cleaned/val')
    test_ds = get_ds('data/cleaned/test')

    # 3. Build Model (VGG16)
    base = tf.keras.applications.VGG16(weights='imagenet', include_top=False, input_shape=(128,128,3))
    base.trainable = False
    
    model = keras.Sequential([
        base,
        layers.GlobalAveragePooling2D(),
        layers.Dense(256, activation='relu'),
        layers.BatchNormalization(),
        layers.Dropout(0.5),
        layers.Dense(1, activation='sigmoid')
    ])

    # 4. Phase 1: Warmup
    model.compile(optimizer=keras.optimizers.Adam(CONFIG['lr']), loss='binary_crossentropy', metrics=['accuracy'])
    print("\n🔥 Phase 1 : Warmup...")
    model.fit(train_ds, validation_data=val_ds, epochs=CONFIG['epochs_warmup'])

    # 5. Phase 2: Fine-Tuning
    base.trainable = True
    model.compile(optimizer=keras.optimizers.Adam(CONFIG['lr']/10), loss='binary_crossentropy', metrics=['accuracy'])
    print("\n❄️ Phase 2 : Fine-tuning...")
    model.fit(train_ds, validation_data=val_ds, epochs=CONFIG['epochs_fine_tune'])

    # 6. Eval
    print("\n📊 Évaluation finale...")
    y_t, y_p = [], []
    for x, y in test_ds:
        y_t.extend(y.numpy())
        y_p.extend(model.predict(x, verbose=0).flatten())
    print(classification_report(np.array(y_t), (np.array(y_p)>0.5).astype(int)))
    
    model.save('model_tl_vgg16.h5')
    print("✅ Sauvegardé : model_tl_vgg16.h5")

if __name__ == "__main__":
    run()
