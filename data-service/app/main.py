from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine
from .routes import predictions

# Créer les tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Data Service - Cancer Detection")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(predictions.router)

@app.get("/health")
def health():
    return {"status": "ok"}
