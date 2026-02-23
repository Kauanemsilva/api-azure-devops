from fastapi import FastAPI
from app.routes import users

app = FastAPI()

# Registrar rotas
app.include_router(users.router)


@app.get("/")
def root():
    return {"message": "API rodando com FastAPI 🚀"}


@app.get("/health")
def health_check():
    return {"status": "ok"}
