from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Modelo de dados
class User(BaseModel):
    id: int
    name: str
    email: str

# Banco fake em memória
users: List[User] = []

@app.get("/")
def root():
    return {"message": "API rodando com FastAPI 🚀"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/users")
def get_users():
    return users

@app.post("/users")
def create_user(user: User):
    users.append(user)
    return {"message": "Usuário criado com sucesso", "user": user}
