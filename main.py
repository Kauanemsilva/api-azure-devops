from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import SessionLocal, User
from azure.monitor.opentelemetry import configure_azure_monitor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
import os
import logging

# 🔥 Configura Azure Monitor
connection_string = os.environ.get("APPLICATIONINSIGHTS_CONNECTION_STRING")

if connection_string:
    configure_azure_monitor(connection_string=connection_string)
    print("✓ Azure Monitor configurado")
else:
    print("⚠ APPLICATIONINSIGHTS_CONNECTION_STRING não encontrada")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# 🔥 Instrumenta automaticamente o FastAPI
FastAPIInstrumentor.instrument_app(app)

class UserModel(BaseModel):
    name: str
    email: str

    class Config:
        from_attributes = True

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
    logger.info("📍 GET / - Raiz da API")
    return {"message": "API rodando com FastAPI 🚀"}

@app.get("/health")
def health_check():
    logger.info("❤️ Health Check - OK")
    return {"status": "ok"}

@app.post("/users")
def create_user(user: UserModel, db: Session = Depends(get_db)):
    logger.info(f"👤 Criando usuário: {user.name}")
    db_user = User(name=user.name, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    users_list = db.query(User).all()
    logger.info(f"📋 Listando {len(users_list)} usuários")
    return users_list