# API Azure DevOps 🚀

API REST desenvolvida em **Python com FastAPI**, com **Pipeline CI/CD automática** usando **GitHub Actions** e **Deploy automático na Microsoft Azure**.

## 📋 Visão Geral

Este projeto demonstra uma arquitetura moderna de **Cloud/DevOps** com:

- ✅ **API REST** completa em Python (FastAPI)
- ✅ **Versionamento** no GitHub
- ✅ **Pipeline de CI/CD** automatizada (GitHub Actions)
- ✅ **Deploy automático** na Azure a cada push
- ✅ **Aplicação rodando online** em ambiente cloud
- ✅ **Testes e validações** automáticas

## 🏗️ Arquitetura do Projeto

```
app/
├── __init__.py
├── main.py                 # Aplicação principal
├── models/
│   ├── __init__.py
│   └── user.py            # Modelos de dados
└── routes/
    ├── __init__.py
    └── users.py           # Endpoints da API
```

## 🔧 Stack Tecnológico

- **Backend**: Python 3.9+
- **Framework**: FastAPI
- **Validação**: Pydantic
- **CI/CD**: GitHub Actions
- **Cloud**: Microsoft Azure (App Service)

## 🚀 Quick Start Local

### Pré-requisitos

- Python 3.9+
- pip
- Git

### 1. Clonar repositório

```bash
git clone https://github.com/seu-usuario/api-azure-devops.git
cd api-azure-devops
```

### 2. Criar ambiente virtual

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4. Executar localmente

```bash
uvicorn app.main:app --reload
```

A API estará disponível em: **http://localhost:8000**

## 📚 Documentação da API

Após executar a aplicação, acesse:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Endpoints Disponíveis

#### Health Check

```http
GET /health
```

Resposta:

```json
{
  "status": "ok"
}
```

#### Listar Usuários

```http
GET /users
```

Resposta:

```json
[
  {
    "id": 1,
    "name": "João Silva",
    "email": "joao@example.com"
  }
]
```

#### Criar Usuário

```http
POST /users
Content-Type: application/json

{
  "id": 1,
  "name": "João Silva",
  "email": "joao@example.com"
}
```

## 🔄 Pipeline CI/CD com GitHub Actions

Toda vez que você faz um `push` para a branch `main`, a pipeline automática:

1. ✅ **Testa** o código
2. 📦 **Constrói** a imagem Docker (ou faz deploy direto)
3. 🚀 **Faz deploy** na Azure App Service
4. 📊 **Valida** se a aplicação está online

### Workflow (.github/workflows/deploy.yml)

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test-and-deploy:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.9"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Run tests (opcional)
        run: |
          pip install pytest
          pytest

      - name: Deploy to Azure
        uses: azure/webapps-deploy@v2
        with:
          app-name: ${{ secrets.AZURE_APP_NAME }}
          publish-profile: ${{ secrets.AZURE_PUBLISH_PROFILE }}
          package: .
```

## 🔐 Configurando Azure & GitHub Actions

### 1. Criar App Service na Azure

```bash
az group create --name myResourceGroup --location eastus

az appservice plan create \
  --name myAppServicePlan \
  --resource-group myResourceGroup \
  --sku B1 --is-linux

az webapp create \
  --resource-group myResourceGroup \
  --plan myAppServicePlan \
  --name api-azure-devops \
  --runtime "PYTHON|3.9"
```

### 2. Obter Publish Profile

```bash
az webapp deployment list-publishing-profiles \
  --resource-group myResourceGroup \
  --name api-azure-devops \
  --query "[0]" > publishprofile.json
```

### 3. Configurar Secrets no GitHub

1. Vá para **Settings > Secrets and variables > Actions**
2. Clique em **New repository secret**
3. Adicione:
   - `AZURE_APP_NAME`: Nome da sua app na Azure
   - `AZURE_PUBLISH_PROFILE`: Conteúdo do `publishprofile.json`

### 4. Criar arquivo de workflow

Crie `.github/workflows/deploy.yml` com o conteúdo acima

## 📤 Fazendo Deploy

Agora é simples: **cada push automático dispara o deploy!**

```bash
# Fazer alterações no código
git add .
git commit -m "Adiciona novo endpoint"
git push origin main

# 🚀 GitHub Actions automaticamente faz o deploy!
```

Acompanhe em: **GitHub > Actions**

## 🔍 Monitorando o Deploy

### No GitHub

- Vá para **Actions** na página do repositório
- Veja o status da pipeline em tempo real

### Na Azure

```bash
# Ver logs da aplicação
az webapp log tail \
  --resource-group myResourceGroup \
  --name api-azure-devops
```

## 📦 requirements.txt

```
fastapi==0.104.1
uvicorn==0.24.0
pydantic==2.5.0
```

## 🧪 Testes (Opcional)

Criar arquivo `test_main.py`:

```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_get_users():
    response = client.get("/users")
    assert response.status_code == 200

def test_create_user():
    response = client.post("/users", json={
        "id": 1,
        "name": "Test User",
        "email": "test@example.com"
    })
    assert response.status_code == 200
```

Executar:

```bash
pytest
```

## 📝 Próximos Passos

- [ ] Adicionar autenticação (JWT)
- [ ] Implementar banco de dados (PostgreSQL)
- [ ] Adicionar testes unitários
- [ ] Configurar logging
- [ ] Adicionar rate limiting
- [ ] Health checks mais completos
- [ ] Documentação de arquitetura
- [ ] GitOps com Terraform

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo LICENSE para detalhes.

## 👤 Autor

**Seu Nome** - [GitHub](https://github.com/seu-usuario)

---

## 🌐 Status

- **API Online**: https://api-azure-devops.azurewebsites.net
- **Documentação**: https://api-azure-devops.azurewebsites.net/docs
- **Status da Última Pipeline**: ![Workflow Status](https://github.com/seu-usuario/api-azure-devops/actions/workflows/deploy.yml/badge.svg)

## 💡 Recursos Adicionais

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [GitHub Actions](https://docs.github.com/en/actions)
- [Azure App Service](https://docs.microsoft.com/en-us/azure/app-service/)
- [Pydantic Documentation](https://docs.pydantic.dev/)

---

**Desenvolvido com ❤️ para demonstrar expertise em Cloud e DevOps**
