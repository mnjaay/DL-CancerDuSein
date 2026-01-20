from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from .database import Base

class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    
    # Infos prédiction essentielles
    prediction = Column(String, nullable=False)  # "Positive" ou "Negative"
    confidence = Column(Float, nullable=False)  # 0.0 à 1.0
    filename = Column(String, nullable=False)
    
    # Timestamp
    created_at = Column(DateTime(timezone=True), server_default=func.now())

