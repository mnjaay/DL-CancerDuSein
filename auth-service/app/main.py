from fastapi import FastAPI, Depends
from sqlalchemy.exc import SQLAlchemyError
from .database import Base, engine, get_db
from .routes import auth

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Auth Service")

app.include_router(auth.router)
