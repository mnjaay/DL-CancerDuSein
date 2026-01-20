from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="API Gateway - Cancer Detection System")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# URLs des services
AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://auth-service:8000")
INFERENCE_SERVICE_URL = os.getenv("INFERENCE_SERVICE_URL", "http://inference-service:8001")
DATA_SERVICE_URL = os.getenv("DATA_SERVICE_URL", "http://data-service:8002")

# Health checks
@app.get("/health")
async def health():
    return {"status": "API Gateway is running"}

# ===== AUTH SERVICE ROUTES =====
@app.post("/api/auth/register")
async def register(request: dict):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{AUTH_SERVICE_URL}/auth/register",
            json=request
        )
        return response.json()

@app.post("/api/auth/login")
async def login(request: dict):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{AUTH_SERVICE_URL}/auth/login",
            json=request
        )
        return response.json()

@app.get("/api/auth/verify")
async def verify_token(token: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{AUTH_SERVICE_URL}/auth/verify",
            params={"token": token}
        )
        return response.json()

# ===== INFERENCE SERVICE ROUTES =====
@app.post("/api/inference/predict")
async def predict(file: UploadFile = File(...)):
    # Lire le contenu du fichier
    file_content = await file.read()
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{INFERENCE_SERVICE_URL}/inference/predict",
            files={"file": (file.filename, file_content, file.content_type)}
        )
        return response.json()

# ===== DATA SERVICE ROUTES - CRUD PREDICTIONS =====

# CREATE
@app.post("/api/predictions")
async def create_prediction(request: dict):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{DATA_SERVICE_URL}/predictions/",
            json=request
        )
        return response.json()

# READ ALL
@app.get("/api/predictions")
async def get_predictions(skip: int = 0, limit: int = 100):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{DATA_SERVICE_URL}/predictions/",
            params={"skip": skip, "limit": limit}
        )
        return response.json()

# READ ONE
@app.get("/api/predictions/{prediction_id}")
async def get_prediction(prediction_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{DATA_SERVICE_URL}/predictions/{prediction_id}"
        )
        return response.json()

# UPDATE
@app.put("/api/predictions/{prediction_id}")
async def update_prediction(prediction_id: int, request: dict):
    async with httpx.AsyncClient() as client:
        response = await client.put(
            f"{DATA_SERVICE_URL}/predictions/{prediction_id}",
            json=request
        )
        return response.json()

# DELETE
@app.delete("/api/predictions/{prediction_id}")
async def delete_prediction(prediction_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.delete(
            f"{DATA_SERVICE_URL}/predictions/{prediction_id}"
        )
        return response.json()

# STATS
@app.get("/api/predictions/stats/summary")
async def get_stats():
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{DATA_SERVICE_URL}/predictions/stats/summary"
        )
        return response.json()

# ===== COMBINED WORKFLOW =====
@app.post("/api/workflow/predict-and-save")
async def predict_and_save(file: UploadFile = File(...)):
    """
    Workflow complet:
    1. Prédire avec le modèle
    2. Sauvegarder dans la base de données
    """
    # Lire le contenu du fichier en bytes
    file_content = await file.read()
    
    # Étape 1: Prédiction
    async with httpx.AsyncClient() as client:
        predict_response = await client.post(
            f"{INFERENCE_SERVICE_URL}/inference/predict",
            files={"file": (file.filename, file_content, file.content_type)}
        )
        prediction_data = predict_response.json()
    
    # Étape 2: Sauvegarder dans data-service
    save_data = {
        "prediction": prediction_data.get("prediction"),
        "confidence": prediction_data.get("confidence"),
        "filename": file.filename
    }
    
    async with httpx.AsyncClient() as client:
        save_response = await client.post(
            f"{DATA_SERVICE_URL}/predictions/",
            json=save_data
        )
    
    return {
        "prediction": prediction_data,
        "saved_record": save_response.json()
    }
