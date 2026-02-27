from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import SessionLocal, User
from azure.monitor.opentelemetry import configure_azure_monitor
import os
import logging

# 🔥 Configura Azure Monitor (Application Insights)
# Só funciona se tiver APPLICATIONINSIGHTS_CONNECTION_STRING no .env
try:
    connection_string = os.environ.get("APPLICATIONINSIGHTS_CONNECTION_STRING")
    if connection_string:
        configure_azure_monitor(connection_string=connection_string)
        print("✓ Azure Monitor configurado")
except Exception as e:
    print(f"⚠ Azure Monitor não configurado: {e}")

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