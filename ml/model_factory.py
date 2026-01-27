import tensorflow as tf
from tensorflow.keras.applications import DenseNet121
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.models import Model

def create_model(input_shape=(128, 128, 3)):
    """
    Crée un modèle basé sur DenseNet121 pour la classification binaire.
    Le modèle de base est gelé, et une tête de classification personnalisée est ajoutée.
    """
    print("Conception du modèle CNN avec Transfer Learning...")

    # 1. Charger un modèle de base pré-entraîné (DenseNet121) sans sa couche de classification supérieure
    base_model = DenseNet121(input_shape=input_shape,
                             include_top=False,
                             weights='imagenet')

    # 2. Geler les couches du modèle de base pré-entraîné
    base_model.trainable = False

    # 3. Créer une nouvelle tête de classification au-dessus du modèle de base gelé
    x = base_model.output
    x = GlobalAveragePooling2D()(x) # Couche de pooling moyen global
    x = Dense(128, activation='relu')(x) # Une couche dense avant la couche de sortie
    output_layer = Dense(1, activation='sigmoid')(x) # Couche dense finale pour la classification binaire

    # 4. Combiner le modèle de base et la tête de classification dans un modèle complet
    model = Model(inputs=base_model.input, outputs=output_layer)
 
    # 5. Compiler le modèle
    # Remarque : Les paramètres d'optimisation comme le taux d'apprentissage peuvent être passés ou ajustés dans train.py généralement,
    # mais ici nous suivons la compilation directe du notebook si elle est simple.
    # Cependant, la compilation se fait généralement à l'extérieur pour pouvoir ajuster le LR.
    # Mais pour correspondre exactement au notebook :
    model.compile(optimizer='adam',
                  loss='binary_crossentropy',
                  metrics=['accuracy'])
    
    return model
