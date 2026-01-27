from tensorflow.keras.models import load_model
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

MODEL_PATH = os.path.join(BASE_DIR, "models", "model.h5")

_model = None


def load_model_once():
    """
    Charge le modèle une seule fois et le garde en cache pour les prédictions futures.
    """
    global _model
    if _model is None:
        _model = load_model(MODEL_PATH)
    return _model
