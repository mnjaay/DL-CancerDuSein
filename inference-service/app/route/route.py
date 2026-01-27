from fastapi import APIRouter, UploadFile, File, HTTPException
from PIL import Image
import httpx
import os
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

CLASS_NAMES = ["Negative", "Positive"]

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

        predicted_class = CLASS_NAMES[int(prediction >= 0.5)]
        confidence = float(prediction if prediction >= 0.5 else 1 - prediction)
        logger.info(f"Classe: {predicted_class}, Confiance: {confidence}")

        return {
            "prediction": predicted_class,
            "confidence": confidence
        }

    except Exception as e:
        logger.error(f"Erreur lors de la prédiction: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

