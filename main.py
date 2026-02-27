from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import SessionLocal, User
from opencensus.ext.azure.log_exporter import AzureLogHandler
import logging
import os

app = FastAPI()


# Modelo Pydantic para Request/Response
class UserModel(BaseModel):
    name: str
    email: str
    
    class Config:
        from_attributes = True


# Dependency para obter sessão do banco
def get_db():
    if not SessionLocal:
        raise Exception("Database not configured")
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "API rodando com FastAPI 🚀"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/users")
def create_user(user: UserModel, db: Session = Depends(get_db)):
    db_user = User(name=user.name, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()


# Configurar logging para Azure Monitor
logger = logging.getLogger(__name__)
logger.addHandler(
    AzureLogHandler(
        connection_string=os.environ["APPLICATIONINSIGHTS_CONNECTION_STRING"]
    )
)
logger.setLevel(logging.INFO)

logger.info("API iniciada com sucesso")