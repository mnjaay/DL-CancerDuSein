from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class PredictionCreate(BaseModel):
    prediction: str
    confidence: float
    filename: str

class PredictionUpdate(BaseModel):
    prediction: Optional[str] = None
    confidence: Optional[float] = None
    filename: Optional[str] = None

class PredictionResponse(BaseModel):
    id: int
    prediction: str
    confidence: float
    filename: str
    created_at: datetime

    class Config:
        from_attributes = True

