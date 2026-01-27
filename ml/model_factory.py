import tensorflow as tf
from tensorflow.keras.applications import DenseNet121
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.models import Model

def create_model(input_shape=(128, 128, 3)):
    """
    Creates a DenseNet121-based model for binary classification.
    The base model is frozen, and a custom classification head is added.
    """
    print("Designing CNN model with Transfer Learning...")

    # 1. Load a pre-trained base model (DenseNet121) without its top classification layer
    base_model = DenseNet121(input_shape=input_shape,
                             include_top=False,
                             weights='imagenet')

    # 2. Freeze the layers of the pre-trained base model
    base_model.trainable = False

    # 3. Create a new classification head on top of the frozen base model
    x = base_model.output
    x = GlobalAveragePooling2D()(x) # Global average pooling layer
    x = Dense(128, activation='relu')(x) # A dense layer before the output layer
    output_layer = Dense(1, activation='sigmoid')(x) # Final dense layer for binary classification

    # 4. Combine the base model and the classification head into a complete Model
    model = Model(inputs=base_model.input, outputs=output_layer)

    # 5. Compile the model
    # Note: Optimization parameters like learning rate can be passed or adjusted in train.py generally,
    # but here we follow the notebook's direct compilation if simple.
    # However, usually compilation happens outside so we can tune LR.
    # But to match notebook exactly:
    model.compile(optimizer='adam',
                  loss='binary_crossentropy',
                  metrics=['accuracy'])
    
    return model
