# 🔧 Guia de Troubleshooting

## Índice

1. [Problemas Comuns](#problemas-comuns)
2. [Erros de Inicialização](#erros-de-inicialização)
3. [Erros de Banco de Dados](#erros-de-banco-dados)
4. [Erros de Deployment](#erros-de-deployment)
5. [Problemas de Performance](#problemas-de-performance)
6. [Problemas de Observabilidade](#problemas-de-observabilidade)

---

## Problemas Comuns

### 1. Porta 8000 já em uso

**Sintoma**:

```
ERROR: [Errno 10048] error while attempting to bind on address ('0.0.0.0', 8000)
winerror 10048: normalmente é permitida apenas uma utilização de cada endereço
```

**Causa**: Outro processo está usando a porta 8000

**Solução (Windows)**:

```bash
# 1. Encontrar processo na porta 8000
netstat -ano | findstr :8000

# 2. Ver qual PID está usando
# Exemplo output: TCP 0.0.0.0:8000 0.0.0.0:0 LISTENING 12345

# 3. Matar processo
taskkill /PID 12345 /F

# 4. Tentar novamente
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

**Solução (macOS/Linux)**:

```bash
# 1. Encontrar
lsof -i :8000

# 2. Matar
kill -9 <PID>

# 3. Ou usar porta diferente
python -m uvicorn main:app --host 0.0.0.0 --port 8001
```

### 2. Módulo não encontrado

**Sintoma**:

```
ModuleNotFoundError: No module named 'fastapi'
ImportError: No module named 'sqlalchemy'
```

**Causa**: Dependências não instaladas

**Solução**:

```bash
# 1. Verificar que ambiente virtual está ativado
which python  # ou where python (Windows)

# 2. Reinstalar dependências
pip install -r requirements.txt

# 3. Verificar versão
pip show fastapi

# 4. Se ainda não funcionar, limpar cache
pip cache purge
pip install -r requirements.txt
```

### 3. Arquivo .env não encontrado

**Sintoma**:

```
⚠ APPLICATIONINSIGHTS_CONNECTION_STRING não configurada
Entity attribute 'DB_USER' not found
```

**Causa**: Arquivo `.env` faltando ou variáveis não configuradas

**Solução**:

```bash
# 1. Copiar exemplo
cp .env.example .env

# 2. Editar .env com valores reais
nano .env  # ou use seu editor favorito
# Configure:
#   DB_SERVER=seu-servidor
#   DB_NAME=seu-banco
#   APPLICATIONINSIGHTS_CONNECTION_STRING=sua-connection

# 3. Verificar se foi criado
ls -la .env

# 4. Testar leitura
python -c "from dotenv import load_dotenv; load_dotenv(); print('OK')"
```

### 4. Aplicação inicia mas não responde

**Sintoma**:

```
Application startup complete
curl http://localhost:8000/health
% Total % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:-- --:--:--(timeout)
```

**Causa**: Servidor não está escutando corretamente

**Solução**:

```bash
# 1. Verificar que server iniciou
# Procure por: "Application startup complete"

# 2. Verificar porta
netstat -ano | findstr :8000
# Deve mostrar LISTENING

# 3. Testar localhost
curl -v http://127.0.0.1:8000/health

# 4. Se não funcionar, reiniciar
# CTRL+C no terminal
# Executar novamente

# 5. Verificar firewall
# Windows Firewall pode estar bloqueando
```

---

## Erros de Inicialização

### Erro: AttributeError na database.py

**Sintoma**:

```
AttributeError: 'module' object has no attribute 'X'
```

**Solução**:

```bash
# 1. Verificar imports em database.py
python -m py_compile database.py

# 2. Se tiver erro de sintaxe, corrigir

# 3. Testar importação isolada
python -c "import database; print('OK')"

# 4. Se error, ver full traceback
python -c "import traceback; import database" 2>&1
```

### Erro: SyntaxError em main.py

**Sintoma**:

```
SyntaxError: invalid syntax (main.py, line XX)
```

**Solução**:

```bash
# 1. Verificar sintaxe
python -m py_compile main.py

# 2. Abrir arquivo e conferir
# - Indentação correta
# - Colchetes/parênteses fechados
# - Sem espaços antes de import

# 3. Usar linter
pip install flake8
flake8 main.py
```

### Erro: CORS bloqueando requisição

**Sintoma**:

```
Access to XMLHttpRequest blocked by CORS policy
Cross-Origin Request Blocked
```

**Solução**:

```python
# Adicionar em main.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todos (dev only!)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Em produção, usar:
allow_origins=[
    "https://seu-dominio.com",
    "https://www.seu-dominio.com"
]
```

---

## Erros de Banco de Dados

### Erro: Azure SQL Connection Failed

**Sintoma**:

```
pyodbc.InterfaceError: ('IM002', '[IM002] [MicrosoftODBC
⚠ Azure SQL indisponível
ℹ Usando SQLite em desenvolvimento local
```

**Status**: ✅ NORMAL (fallback para SQLite funcionando)

**Solução** (se quiser Azure SQL):

```bash
# 1. Verificar credenciais em .env
cat .env | grep DB_

# 2. Testar conexão manualmente
sqlcmd -S seu-servidor.database.windows.net \
       -U seu-usuario \
       -P sua-senha \
       -d seu-banco

# 3. Verificar firewall
# Azure Portal > SQL Server > Firewall settings
# Adicionar seu IP

# 4. Se conexão ainda falhar, use SQLite (dev)
# O sistema já faz fallback automático!
```

### Erro: Database locked (SQLite)

**Sintoma**:

```
sqlite3.OperationalError: database is locked
```

**Causa**: Multiple processes acessando SQLite simultaneamente

**Solução**:

```python
# Em database.py, melhorar timeout
engine = create_engine(
    "sqlite:///./test.db",
    connect_args={
        "check_same_thread": False,
        "timeout": 30  # Aumentar timeout
    },
    pool_pre_ping=True,  # Validar conexões
    echo=False
)
```

### Erro: Email duplicado

**Sintoma**:

```
IntegrityError: (psycopg2.IntegrityError) duplicate key value violates unique constraint "users_email_key"
```

**Causa**: Email já existe no banco

**Solução**:

```python
# Em main.py, adicionar tratamento
from sqlalchemy.exc import IntegrityError

@app.post("/users")
def create_user(user: UserModel, db: Session = Depends(get_db)):
    try:
        db_user = User(name=user.name, email=user.email)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError:
        db.rollback()
        return {"error": "Email já existe"}
```

---

## Erros de Deployment

### Erro: GitHub Actions falha

**Sintoma**:

```
❌ Build job failed
See logs for details
```

**Solução**:

```bash
# 1. Ver logs completos
GitHub > Actions > [workflow] > Logs

# 2. Causas comuns:
# - requirements.txt com versões incompatíveis
# - Teste falhando
# - Erro de sintaxe

# 3. Verificar localmente
pip install -r requirements.txt
pytest
python -m py_compile main.py

# 4. Fazer commit com correção
git add .
git commit -m "fix: Corrige erro de build"
git push origin main
```

### Erro: Deploy timeout

**Sintoma**:

```
Deploy exceeded 30 minute timeout
```

**Causa**: Build levando muito tempo

**Solução**:

```bash
# 1. Otimizar requirements.txt
# Remover pacotes desnecessários

# 2. Usar menos logs durante build
# Em .github/workflows/..., adicionar
--quiet

# 3. Aumentar timeout em Azure
# App Service > Deployment Center
# Configure timeout
```

### Erro: Authentication failed

**Sintoma**:

```
ERROR: AZUREAPPSERVICE_CLIENTID not found
fatal: Authentication failed for ...
```

**Solução**:

```bash
# 1. Verificar secrets no GitHub
GitHub > Settings > Secrets and variables > Actions

# 2. Certificar que existem:
# - AZUREAPPSERVICE_CLIENTID
# - AZUREAPPSERVICE_TENANTID
# - AZUREAPPSERVICE_SUBSCRIPTIONID

# 3. Se não existem, criar via Azure CLI
az ad sp create-for-rbac \
  --name "api-fastapi-kauane" \
  --role contributor \
  --scopes /subscriptions/{subscription-id}

# 4. Adicionar secrets no GitHub

# 5. Novo push para testar
git commit --allow-empty -m "Trigger deploy"
git push origin main
```

---

## Problemas de Performance

### API Lenta

**Sintoma**:

```
Response time > 1000ms
Timeout ao fazer requisições
```

**Diagnóstico**:

```bash
# 1. Verificar CPU/Memory
Azure Portal > App Service > CPU percentage
Azure Portal > App Service > Memory percentage

# 2. Verificar database
query = db.query(User)
print(f"Query execution: {datetime.now()}")

# 3. Verificar requests/sec
Application Insights > Logs > requests
```

**Solução**:

```python
# 1. Adicionar cache
from functools import lru_cache

@lru_cache(maxsize=128)
def get_users_cached(db):
    return db.query(User).all()

# 2. Otimizar query
# ❌ Lento
users = db.query(User).all()

# ✅ Rápido
users = db.query(User).limit(100).all()

# 3. Adicionar índices
# Em database.py
__table_args__ = (Index('idx_users_email', 'email'),)

# 4. Connection pooling
engine = create_engine(
    DB_URL,
    pool_size=20,
    max_overflow=40,
    pool_recycle=3600,
)
```

### CPU Alto

**Solução**:

```bash
# 1. Ver qual processo está consumindo
Azure Portal > Diagnostics > CPU Analysis

# 2. Aumentar App Service Plan
# De B1 para B2 ou S1

# 3. Enabler auto-scaling
az monitor autoscale create \
  --resource-group myResourceGroup \
  --resource-name myAppServicePlan \
  --resource-type "Microsoft.Web/serverfarms" \
  --min-count 1 \
  --max-count 3
```

### Memory High

**Solução**:

```python
# 1. Verificar memory leaks
# Usar memory_profiler
pip install memory-profiler

@profile
def get_users(db):
    return db.query(User).all()

# 2. Limpar dados não usados
db.expire_all()
gc.collect()

# 3. Usar streaming para grandes datasets
def get_large_dataset(db):
    for user in db.query(User).yield_per(100):
        yield user
```

---

## Problemas de Observabilidade

### Logs não aparecem

**Sintoma**:

```
Application Insights > Logs > traces
Sem resultados para últimas 24h
```

**Causa**: Connection string inválida ou não configurada

**Solução**:

```bash
# 1. Verificar .env
cat .env | grep APPLICATIONINSIGHTS_CONNECTION_STRING

# 2. Validar format
# Deve conter:
# - InstrumentationKey=...
# - IngestionEndpoint=https://...
# - LiveEndpoint=https://...
# - ApplicationId=...

# 3. Se inválida, atualizar
# Azure Portal > Application Insights
# Share > Settings > Properties
# Copiar Connection String

# 4. Atualizar .env
nano .env
# APPLICATIONINSIGHTS_CONNECTION_STRING=<novo-valor>

# 5. Reiniciar aplicação
# CTRL+C
# python -m uvicorn main:app --reload

# 6. Fazer requisição de teste
curl http://localhost:8000/health

# 7. Aguardar 30-60 segundos
# Traces aparecem em Application Insights
```

### Alertas não funcionam

**Solução**:

```bash
# 1. Verificar se alerta está enabled
Azure Portal > Monitor > Rules
# Status deve ser "Enabled"

# 2. Verificar Action Group
Azure Portal > Monitor > Action Groups
# Verificar email configurado

# 3. Forçar condição para testar
# Se alerta é "CPU > 80%", sobrecarregar CPU

# 4. Ver histórico
Azure Portal > Monitor > Alerts > Alert History
# Verificar se foi acionado

# 5. Se não funciona, recriar
az monitor metrics alert create \
  --resource-group myResourceGroup \
  --name "High CPU Alert"
```

### Dashboards em branco

**Solução**:

```bash
# 1. Aguardar dados serem coletados
# Mínimo 5 minutos de dados

# 2. Verificar data/hora
# Painel pode estar mostrando período sem dados

# 3. Fazer requisições
curl http://localhost:8000/health
curl http://localhost:8000/users

# 4. Aguardar 1-2 minutos
# Dados aparecerem no dashboard
```

---

## Checklist de Debug

Quando algo não funciona:

```
☐ Verificar logs do servidor
  tail -f /var/log/app.log

☐ Verificar porta
  netstat -ano | findstr :8000

☐ Verificar ambiente virtual
  which python

☐ Verificar .env
  cat .env | grep DB_

☐ Verificar banco de dados
  python -c "import database; print('OK')"

☐ Verificar Application Insights
  Azure Portal > Application Insights > Logs

☐ Verificar Azure SQL
  sqlcmd -S servidor.database.windows.net -U usuario

☐ Verificar deployment logs
  az webapp log tail -g myResourceGroup -n api-fastapi-kauane

☐ Verificar health check
  curl https://api-fastapi-kauane.azurewebsites.net/health

☐ Verificar GitHub Actions logs
  GitHub > Actions > Latest Workflow > Logs
```

---

## Contato & Suporte

- **GitHub Issues**: [Abrir issue](https://github.com/seu-usuario/api-azure-devops/issues)
- **Azure Support**: https://portal.azure.com/#view/Microsoft_Azure_Support/NewSupportRequest
- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **SQLAlchemy Docs**: https://docs.sqlalchemy.org/

---

> Não encontrou sua solução? Abra uma issue com:
>
> - Erro exato
> - Passos para reproduzir
> - Logs (sem credenciais!)
