from fastapi import APIRouter
from typing import List
from app.models import User

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

# Banco fake em memória
users: List[User] = []


@router.get("")
def get_users():
    return users


@router.post("")
def create_user(user: User):
    users.append(user)
    return {"message": "Usuário criado com sucesso", "user": user}
