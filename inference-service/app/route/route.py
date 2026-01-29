from fastapi import APIRouter, UploadFile, File, HTTPException
from PIL import Image
import httpx
import os
import json
import logging
from io import BytesIO
from dotenv import load_dotenv

from ..utils.preprocess import preprocess_image
from ..utils.model_loader import load_model_once

load_dotenv()

# Configurer le logging
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/inference", tags=["inference"])

model = load_model_once()

# Charger le mapping des classes dynamiquement
def load_class_names():
    try:
        classes_path = os.path.join(os.path.dirname(__file__), "..", "..", "models", "classes.json")
        if os.path.exists(classes_path):
            with open(classes_path, 'r') as f:
                labels = json.load(f)
                # On convertit les clés en int et on trie pour avoir une liste [label_0, label_1]
                return [labels[str(i)] for i in sorted(map(int, labels.keys()))]
    except Exception as e:
        logger.error(f"Erreur lors du chargement des classes: {e}")
    
    # Fallback par défaut (au cas où)
    return ["Positive", "Negative"]

CLASS_NAMES = load_class_names()
logger.info(f"Classes chargées: {CLASS_NAMES}")

# URL du service data
# URL du service data
DATA_SERVICE_URL = os.getenv("DATA_SERVICE_URL", "http://data-service:8002")
if not DATA_SERVICE_URL.startswith("http://") and not DATA_SERVICE_URL.startswith("https://"):
    DATA_SERVICE_URL = f"http://{DATA_SERVICE_URL}"


@router.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        logger.info(f"Reçu fichier: {file.filename}")
        
        # Lire le contenu du fichier
        file_content = await file.read()
        logger.info(f"Fichier lu: {len(file_content)} bytes")
        
        # Ouvrir l'image directement à partir des bytes
        image = Image.open(BytesIO(file_content))
        logger.info(f"Image ouverte: {image.size}, mode: {image.mode}")
        
        image_array = preprocess_image(image)
        logger.info(f"Image prétraitée: {image_array.shape}")

        prediction = model.predict(image_array)[0][0]
        logger.info(f"Prédiction brute: {prediction}")

        predicted_class_raw = CLASS_NAMES[int(prediction >= 0.5)]
        
        # Mapping logique pour l'utilisateur :
        # Si la classe détectée est "Cancer", on renvoie "Positive"
        # Si la classe détectée est "Negative", on renvoie "Negative"
        if predicted_class_raw.lower() == "cancer":
            predicted_class = "Positive"
        else:
            predicted_class = predicted_class_raw

        confidence = float(prediction if prediction >= 0.5 else 1 - prediction)
        logger.info(f"Classe brute: {predicted_class_raw} -> Finale: {predicted_class}, Confiance: {confidence}")

        return {
            "prediction": predicted_class,
            "confidence": confidence
        }

    except Exception as e:
        logger.error(f"Erreur lors de la prédiction: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

