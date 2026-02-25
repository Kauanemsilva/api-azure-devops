import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestHealthCheck:
    def test_health_check(self):
        """Testa se a API está saudável"""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"


class TestRootEndpoint:
    def test_root_endpoint(self):
        """Testa endpoint raiz"""
        response = client.get("/")
        assert response.status_code == 200
        assert "message" in response.json()


class TestUsersEndpoint:
    def test_get_users_empty(self):
        """Testa listagem de usuários vazia"""
        response = client.get("/users")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_create_user(self):
        """Testa criação de novo usuário"""
        user_data = {
            "id": 1,
            "name": "João Silva",
            "email": "joao@example.com"
        }
        response = client.post("/users", json=user_data)
        assert response.status_code == 200
        assert "message" in response.json()
        assert response.json()["user"]["name"] == "João Silva"
    
    def test_create_and_list_users(self):
        """Testa criar e listar usuários"""
        # Criar usuário
        user_data = {
            "id": 2,
            "name": "Maria Santos",
            "email": "maria@example.com"
        }
        response = client.post("/users", json=user_data)
        assert response.status_code == 200
        
        # Listar usuários
        response = client.get("/users")
        assert response.status_code == 200
        users = response.json()
        assert len(users) > 0
