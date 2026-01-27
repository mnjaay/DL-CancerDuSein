import numpy as np
from PIL import Image

IMG_SIZE = (128, 128)

def preprocess_image(image: Image.Image):
    """
    Prétraite l'image pour l'inférence : conversion RGB, redimensionnement,
    normalisation et ajout d'une dimension de batch.
    """
    image = image.convert("RGB")
    image = image.resize(IMG_SIZE)
    image = np.array(image) / 255.0
    image = np.expand_dims(image, axis=0)
    return image
