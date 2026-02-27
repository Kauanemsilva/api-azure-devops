from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import SessionLocal, User
from azure.monitor.opentelemetry import configure_azure_monitor
from opentelemetry import trace
import os
import logging
from datetime import datetime

# 🔥 Configura Azure Monitor (Application Insights)
connection_string = os.environ.get("APPLICATIONINSIGHTS_CONNECTION_STRING")

try:
    if connection_string:
        # Configurar Azure Monitor com OpenTelemetry
        configure_azure_monitor(connection_string=connection_string)
        
        # Pegar tracer para rastreamento
        tracer = trace.get_tracer(__name__)
        
        print("✓ Azure Monitor conectado com sucesso!")
        print(f"✓ Enviando dados para Application Insights (Canada Central)")
    else:
        print("⚠ APPLICATIONINSIGHTS_CONNECTION_STRING não configurada no .env")
        tracer = None
except Exception as e:
    print(f"❌ Erro ao configurar Azure Monitor: {e}")
    tracer = None

# Configurar logging local para debug
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    logger.info("📍 GET / - Raiz da API")
    return {"message": "API rodando com FastAPI 🚀"}


@app.get("/health")
def health_check():
    logger.info("❤️ Health Check - OK")
    return {"status": "ok"}


@app.post("/users")
def create_user(user: UserModel, db: Session = Depends(get_db)):
    logger.info(f"👤 Criando usuário: {user.name} ({user.email})")
    db_user = User(name=user.name, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    logger.info(f"✅ Usuário criado com ID: {db_user.id}")
    return db_user


@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    users_list = db.query(User).all()
    logger.info(f"📋 Listando {len(users_list)} usuários")
    return users_list