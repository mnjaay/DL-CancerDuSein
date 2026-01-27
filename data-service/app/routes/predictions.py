from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Prediction
from ..schemas import PredictionCreate, PredictionUpdate, PredictionResponse
from typing import List

router = APIRouter(prefix="/predictions", tags=["predictions"])

# CREATE - Ajouter une prédiction
@router.post("/", response_model=PredictionResponse)
def create_prediction(prediction: PredictionCreate, db: Session = Depends(get_db)):
    """
    Crée une nouvelle entrée de prédiction dans la base de données.
    """
    try:
        db_prediction = Prediction(**prediction.dict())
        db.add(db_prediction)
        db.commit()
        db.refresh(db_prediction)
        return db_prediction
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

# READ - Récupérer toutes les prédictions
@router.get("/", response_model=List[PredictionResponse])
def get_predictions(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Récupère une liste de prédictions avec pagination.
    """
    return db.query(Prediction).offset(skip).limit(limit).all()

# READ - Récupérer une prédiction par ID
@router.get("/{prediction_id}", response_model=PredictionResponse)
def get_prediction(prediction_id: int, db: Session = Depends(get_db)):
    db_prediction = db.query(Prediction).filter(Prediction.id == prediction_id).first()
    if not db_prediction:
        raise HTTPException(status_code=404, detail="Prédiction non trouvée")
    return db_prediction

# UPDATE - Modifier une prédiction
@router.put("/{prediction_id}", response_model=PredictionResponse)
def update_prediction(
    prediction_id: int,
    prediction: PredictionUpdate,
    db: Session = Depends(get_db)
):
    db_prediction = db.query(Prediction).filter(Prediction.id == prediction_id).first()
    if not db_prediction:
        raise HTTPException(status_code=404, detail="Prédiction non trouvée")
    
    update_data = prediction.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_prediction, field, value)
    
    try:
        db.commit()
        db.refresh(db_prediction)
        return db_prediction
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

# DELETE - Supprimer une prédiction
@router.delete("/{prediction_id}")
def delete_prediction(prediction_id: int, db: Session = Depends(get_db)):
    db_prediction = db.query(Prediction).filter(Prediction.id == prediction_id).first()
    if not db_prediction:
        raise HTTPException(status_code=404, detail="Prédiction non trouvée")
    
    try:
        db.delete(db_prediction)
        db.commit()
        return {"message": "Prédiction supprimée"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

# BONUS - Statistiques
@router.get("/stats/summary")
def get_stats(db: Session = Depends(get_db)):
    """
    Génère un résumé statistique des prédictions (total, positifs, négatifs).
    """
    total = db.query(Prediction).count()
    positive = db.query(Prediction).filter(Prediction.prediction == "Positive").count()
    negative = db.query(Prediction).filter(Prediction.prediction == "Negative").count()
    
    return {
        "total": total,
        "positive": positive,
        "negative": negative,
        "positive_percentage": (positive / total * 100) if total > 0 else 0
    }

