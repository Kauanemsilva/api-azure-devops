# 📚 Documentação Completa - API Azure DevOps

## Índice

1. [Visão Geral do Projeto](#visão-geral)
2. [Arquitetura Técnica](#arquitetura-técnica)
3. [Componentes do Sistema](#componentes)
4. [Stack Tecnológico](#stack-tecnológico)
5. [Endpoints da API](#endpoints)
6. [Banco de Dados](#banco-dados)
7. [Observabilidade](#observabilidade)
8. [Segurança](#segurança)

---

## Visão Geral

### O Que É?

Esta é uma **API REST profissional** desenvolvida para demonstrar expertise em:

- **Cloud Computing** (Microsoft Azure)
- **DevOps** (CI/CD automático)
- **Arquitetura de Software** (Clean Code, modularização)
- **Observabilidade** (Logs, Traces, Metrics)

### Status Atual

```
✅ API rodando em produção
✅ Banco de dados conectado
✅ Observabilidade ativa
✅ CI/CD automático
✅ Monitoramento 24/7
```

### Localização

- **URL da API**: https://api-fastapi-kauane.azurewebsites.net
- **Documentação Interativa**: https://api-fastapi-kauane.azurewebsites.net/docs
- **Repositório**: https://github.com/seu-usuario/api-azure-devops

---

## Arquitetura Técnica

### Diagrama de Fluxo

```
┌─────────────────────────────────────────────────────────────────┐
│                     LOCAL DEVELOPMENT                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Developer Machine                                               │
│  ┌──────────────────┐                                            │
│  │ Python 3.10+     │                                            │
│  │ FastAPI          │  (com hot reload)                          │
│  │ SQLite           │                                            │
│  └────────┬─────────┘                                            │
│           │ git push                                             │
│           ▼                                                       │
└──────────────────────────────────────────────────────────────────┘
            │
            ▼
┌──────────────────────────────────────────────────────────────────┐
│                     GITHUB REPOSITORY                            │
├──────────────────────────────────────────────────────────────────┤
│  - Source code version control                                   │
│  - Triggers GitHub Actions on push                               │
│  - Stores secrets securely                                       │
└──────┬───────────────────────────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────────────────────────────┐
│                    GITHUB ACTIONS (CI/CD)                        │
├──────────────────────────────────────────────────────────────────┤
│  1. Checkout código                                              │
│  2. Setup Python 3.10                                            │
│  3. Instalar dependências (pip install)                          │
│  4. Validar/Testar código                                        │
│  5. Build artifacts                                              │
│  6. Push para Azure                                              │
└──────┬───────────────────────────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────────────────────────────┐
│                 AZURE CLOUD INFRASTRUCTURE                       │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Web App (Container App)                                  │  │
│  │ - Python 3.10 Runtime                                    │  │
│  │ - Uvicorn ASGI Server                                    │  │
│  │ - Auto-scaling habilitado                                │  │
│  │ - Health checks cada 1 minuto                            │  │
│  └─────────────────┬──────────────────────────────────────┬─┘  │
│                    │ Logs/Metrics                         │     │
│  ┌─────────────────▼──────────────────┐  ┌──────────────▼─┐   │
│  │ Azure SQL Database                 │  │ Application    │   │
│  │ - Backups automáticos              │  │ Insights       │   │
│  │ - Replicação enable                │  │ - Traces       │   │
│  │ - Firewall configurado             │  │ - Metrics      │   │
│  │ - Connection pooling               │  │ - Alerts       │   │
│  └────────┬─────────────────────────┼──┴────────────┬────┘   │
│           │                         │                │         │
│           └─────────┬───────────────┴────────────┬───┘         │
│                     │                           │              │
│                     ▼                           ▼              │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Azure Monitor & Alertas                                  │  │
│  │ - Alertas em tempo real                                  │  │
│  │ - Dashboards customizados                                │  │
│  │ - Análise de tendências                                  │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## Componentes

### 1. Web App (Azure App Service)

**Responsável por**: Hospedar a aplicação Python

**Configuração**:

- Runtime: Python 3.10
- Servidor: Uvicorn 0.41.0
- Processamento: Async/Multi-thread
- Auto-scaling: Habilitado
- Health checks: Cada 1 minuto

**Monitoramento**:

```
Métricas rastreadas:
- CPU usage (%)
- Memory usage (MB)
- Requests (por segundo)
- Response time (ms)
- Error rate (%)
```

### 2. Azure SQL Database

**Responsável por**: Persistência de dados

**Configuração**:

- Versão: SQL Server 2019
- Tier: Standard (S0/S1/S2)
- Backup: Automático a cada 5 minutos
- Replicação: Habilitada
- Firewall: Regras configuradas

**Tabelas**:

```sql
-- Tabela principal
CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(255) NOT NULL,
  email VARCHAR(255) UNIQUE NOT NULL
);

-- Índices
CREATE INDEX idx_users_email ON users(email);
```

### 3. Application Insights

**Responsável por**: Telemetria e observabilidade

**Dados Coletados**:

- Requests (entrada/saída)
- Traces (logs estruturados)
- Exceptions (erros)
- Metrics (CPU, memória)
- Custom Events (eventos custom)

**Retenção**: 90 dias (padrão)

### 4. Azure Monitor

**Responsável por**: Alertas e monitoramento

**Alerts Configuradas**:

1. **High CPU** (> 80% por 5 min)
2. **High Memory** (> 90% por 5 min)
3. **Error Rate** (> 5% por 1 min)
4. **Response Time** (> 1000ms por 5 min)

---

## Stack Tecnológico

### Backend

```yaml
Python:
  Version: 3.10+
  Package Manager: pip

Framework:
  FastAPI: 0.131.0
    - Modern async web framework
    - Built-in dependency injection
    - Request validation with Pydantic
    - Automatic API docs (Swagger/ReDoc)

Server:
  Uvicorn: 0.41.0
    - ASGI web server
    - HTTP/1.1 e WebSocket support
    - Auto-reload (dev mode)

ORM:
  SQLAlchemy: 2.0.23
    - Object-relational mapping
    - Connection pooling
    - Query builder
    - ORM Session management

Validation:
  Pydantic: 2.12.5
    - Data validation and parsing
    - Type hints support
    - Custom validators
```

### Cloud & DevOps

```yaml
Cloud Provider:
  Microsoft Azure:
    - Web App (App Service)
    - SQL Database
    - Application Insights
    - Azure Monitor

CI/CD:
  GitHub:
    - Repository hosting
    - Secrets management
    - Actions workflow
    - Code review

  GitHub Actions:
    - Automated testing
    - Build automation
    - Deploy automation
```

### Observabilidade

```yaml
Logging:
  Python logging: Built-in

Tracing:
  OpenTelemetry: Via Azure Monitor

Metrics:
  Application Insights: Automático

Monitoring:
  Azure Monitor: 24/7
```

---

## Endpoints

### 1. GET / - Root

**Descrição**: Retorna status da API

**URL**: `GET /`

**Response**:

```json
{
  "message": "API rodando com FastAPI 🚀"
}
```

**Status Codes**:

- `200 OK` - Sucesso

---

### 2. GET /health - Health Check

**Descrição**: Verifica saúde da API

**URL**: `GET /health`

**Response**:

```json
{
  "status": "ok"
}
```

**Status Codes**:

- `200 OK` - API saudável

**Uso**: Monitoramento de uptime, load balancers

---

### 3. GET /users - Listar Usuários

**Descrição**: Retorna lista de todos os usuários

**URL**: `GET /users`

**Query Parameters**: Nenhum

**Response**:

```json
[
  {
    "id": 1,
    "name": "João Silva",
    "email": "joao@example.com"
  },
  {
    "id": 2,
    "name": "Maria Santos",
    "email": "maria@example.com"
  }
]
```

**Status Codes**:

- `200 OK` - Sucesso
- `500 Internal Server Error` - Erro ao conectar ao banco

---

### 4. POST /users - Criar Usuário

**Descrição**: Cria um novo usuário

**URL**: `POST /users`

**Request Body**:

```json
{
  "name": "João Silva",
  "email": "joao@example.com"
}
```

**Response**:

```json
{
  "id": 3,
  "name": "João Silva",
  "email": "joao@example.com"
}
```

**Status Codes**:

- `200 OK` - Usuário criado com sucesso
- `422 Unprocessable Entity` - Dados inválidos
- `500 Internal Server Error` - Erro ao salvar

**Validações**:

- `name`: String não vazia (required)
- `email`: Formato válido de e-mail (required, unique)

---

## Banco de Dados

### Conexão Dual

**Desenvolvimento** (Fallback):

```python
DATABASE_URL = "sqlite:///./test.db"
```

**Produção**:

```python
DATABASE_URL = f"mssql+pyodbc://{user}:{password}@{server}/{database}?driver=ODBC+Driver+18+for+SQL+Server"
```

### User Model

```python
class User(Base):
    __tablename__ = "users"

    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String, nullable=False)
    email: str = Column(String, unique=True, nullable=False)
```

### Operações com SQLAlchemy

```python
# Criar (CREATE)
user = User(name="João", email="joao@example.com")
db.add(user)
db.commit()
db.refresh(user)

# Ler (READ)
users = db.query(User).all()
user = db.query(User).filter(User.id == 1).first()

# Atualizar (UPDATE)
user.name = "João Silva"
db.commit()

# Deletar (DELETE)
db.delete(user)
db.commit()
```

---

## Observabilidade

### Application Insights

**Logs Estruturados**:

```
TRACE (Nível): "📍 GET / - Raiz da API"
TRACE (Nível): "❤️ Health Check - OK"
TRACE (Nível): "👤 Criando usuário: João"
TRACE (Nível): "📋 Listando 3 usuários"
```

**Query KQL (Kusto)**:

```kusto
// Últimos 100 logs
traces
| order by timestamp desc
| limit 100

// Contar por severidade
traces
| summarize count() by severidade = severity

// Performance por endpoint
requests
| summarize
    avg_duration = avg(duration),
    max_duration = max(duration),
    count = count()
  by tostring(url)
```

### Métricas

**Disponíveis em tempo real**:

- Requests por segundo
- Tempo de resposta médio
- Taxa de erro (%)
- CPU usage (%)
- Memory usage (MB)
- Disk I/O

### Alertas Configuradas

```
Alert 1: High CPU Usage
- Threshold: CPU > 80%
- Duration: 5 minutos
- Action: Notification → Email

Alert 2: High Memory Usage
- Threshold: MEM > 90%
- Duration: 5 minutos
- Action: Notification → Email

Alert 3: High Error Rate
- Threshold: Erros > 5%
- Duration: 1 minuto
- Action: Notification → Email, PagerDuty

Alert 4: Slow Response Time
- Threshold: Response > 1000ms
- Duration: 5 minutos
- Action: Notification → Email
```

---

## Segurança

### Variáveis de Ambiente

**Arquivo `.env` (NÃO COMMITAR)**:

```env
# Database
DB_SERVER=dbapidevops.database.windows.net
DB_NAME=dbapidevops
DB_USER=seu-usuario
DB_PASSWORD=sua-senha-forte
DB_DRIVER=ODBC Driver 18 for SQL Server

# Azure Monitor
APPLICATIONINSIGHTS_CONNECTION_STRING=InstrumentationKey=...
```

### GitHub Secrets

**Configurar em**: Settings > Secrets and variables > Actions

```
AZUREAPPSERVICE_CLIENTID = 12345678-...
AZUREAPPSERVICE_TENANTID = 87654321-...
AZUREAPPSERVICE_SUBSCRIPTIONID = abcdef12-...
```

### CORS (Cross-Origin)

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://seu-dominio.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### HTTPS

**Automático no Azure**:

```
https://api-fastapi-kauane.azurewebsites.net
```

### Rate Limiting

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.get("/users")
@limiter.limit("100/minute")
async def get_users(request: Request, db: Session = Depends(get_db)):
    pass
```

---

## Próximos Passos

- [ ] Autenticação JWT
- [ ] Rate limiting
- [ ] Cache com Redis
- [ ] WebSocket support
- [ ] GraphQL API
- [ ] Kubernetes deployment
- [ ] Terraform IaC
- [ ] Load testing com k6
