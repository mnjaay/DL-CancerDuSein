from fastapi import FastAPI
from .route.route import router as api_router
app = FastAPI(
    title="Cancer Detection API",
    description="API de classification d’images pour le cancer du sein (CNN)",
    
)

# Charger les routes
app.include_router(api_router)


@app.get("/")
def root():
    return {
        "message": "L'API de détection du cancer est en cours d'exécution."
    }
