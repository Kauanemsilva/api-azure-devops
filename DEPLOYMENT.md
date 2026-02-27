# 🚀 Guia Completo de Deployment

## Índice

1. [Opções de Deploy](#opções-de-deploy)
2. [Deploy Automático (GitHub Actions)](#deploy-automático)
3. [Deploy Manual (Azure CLI)](#deploy-manual)
4. [Configurações Pós-Deploy](#configurações-pós-deploy)
5. [Monitoramento do Deploy](#monitoramento)

---

## Opções de Deploy

### 1. Deploy Automático ✅ RECOMENDADO

```
Tecnologia: GitHub Actions
Trigger: git push origin main
Tempo: ~5 minutos
Downtime: 0 (zero)
```

### 2. Deploy Manual

```
Tecnologia: Azure CLI / Azure Portal
Trigger: Comando manual
Tempo: ~3 minutos
Downtime: Depende do método
```

### 3. Deploy com Docker

```
Tecnologia: Docker Container
Trigger: Manual
Tempo: ~10 minutos
Downtime: Manter
```

---

## Deploy Automático

### Como Funciona

1. **Developer faz push**

   ```bash
   git push origin main
   ```

2. **GitHub Actions é acionado**
   - Webhook automático ativa o workflow

3. **Pipeline executa**
   - Checkout código
   - Setup Python 3.10
   - Instalar dependências
   - Rodar testes
   - Build artifacts

4. **Deploy na Azure**
   - Login com credentials
   - Deploy para Web App
   - Health checks

5. **Resultado**
   - ✅ API online
   - 📊 Logs em Application Insights
   - 🔔 Alertas ativos

### Workflow Configurado

**Arquivo**: `.github/workflows/main_api-fastapi-kauane.yml`

```yaml
name: Build and deploy Python app to Azure Web App

on:
  push:
    branches:
      - main
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.10"

      - name: Install dependencies
        run: |
          python -m venv venv
          source venv/bin/activate
          pip install -r requirements.txt

      - name: Upload artifact
        uses: actions/upload-artifact@v4
        with:
          name: python-app
          path: |
            .
            !venv/

  deploy:
    runs-on: ubuntu-latest
    needs: build

    steps:
      - name: Download artifact
        uses: actions/download-artifact@v4
        with:
          name: python-app

      - name: Login to Azure
        uses: azure/login@v2
        with:
          client-id: ${{ secrets.AZUREAPPSERVICE_CLIENTID }}
          tenant-id: ${{ secrets.AZUREAPPSERVICE_TENANTID }}
          subscription-id: ${{ secrets.AZUREAPPSERVICE_SUBSCRIPTIONID }}

      - name: Deploy to Azure Web App
        uses: azure/webapps-deploy@v3
        with:
          app-name: "api-fastapi-kauane"
          slot-name: "Production"
```

### Fazer Deploy (Automático)

```bash
# 1. Fazer alterações no código
echo "# Nova feature" >> README.md

# 2. Commit e push
git add .
git commit -m "feat: Adiciona nova feature"
git push origin main

# 3. Aguardar ~5 minutos
# GitHub Actions está trabalhando!

# 4. Acompanhar em tempo real
# GitHub > Actions > Último workflow

# 5. Verificar resultado
curl https://api-fastapi-kauane.azurewebsites.net/health
```

### Acompanhar Deploy

**No GitHub**:

```
GitHub > Actions > meu-repositório > Workflow runs
```

Vizualizar:

- ✅/❌ Status de cada job
- ⏱️ Duração
- 📊 Logs
- 🔴 Erros (se houver)

**No Azure Portal**:

```
Azure Portal > App Service > Deployment center > Build history
```

Vizualizar:

- Status do deploy
- Logs de deployment
- Versão deployada

---

## Deploy Manual

### Pré-requisitos

```bash
# 1. Instalar Azure CLI
# Windows: https://learn.microsoft.com/en-us/cli/azure/install-azure-cli-windows

# 2. Fazer login
az login

# 3. Verificar assinatura
az account show
```

### Opção 1: Azure CLI (Recomendado)

```bash
# 1. Criar grupo de recursos (se não existir)
az group create \
  --name myResourceGroup \
  --location canadacentral

# 2. Criar plano App Service
az appservice plan create \
  --name myAppServicePlan \
  --resource-group myResourceGroup \
  --sku B1 \
  --is-linux

# 3. Criar Web App
az webapp create \
  --resource-group myResourceGroup \
  --plan myAppServicePlan \
  --name api-fastapi-seu-nome \
  --runtime "PYTHON|3.10"

# 4. Configurar variáveis de ambiente
az webapp config appsettings set \
  --resource-group myResourceGroup \
  --name api-fastapi-seu-nome \
  --settings \
    APPLICATIONINSIGHTS_CONNECTION_STRING="sua-connection-string" \
    DB_SERVER="seu-servidor" \
    DB_NAME="seu-banco"

# 5. Deploy
az webapp up \
  --resource-group myResourceGroup \
  --name api-fastapi-seu-nome \
  --runtime "PYTHON:3.10" \
  --logs
```

### Opção 2: Azure Portal

1. **Criar Web App**

   ```
   Azure Portal > Create a resource > Web App
   ```

2. **Configurar**
   - Name: `api-fastapi-seu-nome`
   - Runtime: Python 3.10
   - Region: Canada Central

3. **Deploy**

   ```
   Deployment center > GitHub Actions
   ```

4. **Conectar repositório**
   - Selecionar organization
   - Selecionar repositório
   - Selecionar branch (main)

5. **Workflow criado automaticamente**
   - Arquivo gerado em `.github/workflows/`
   - Próximo push dispara deploy

### Opção 3: Docker

```bash
# 1. Build image
docker build -t api-fastapi:latest .

# 2. Testar localmente
docker run -p 8000:8000 \
  -e APPLICATIONINSIGHTS_CONNECTION_STRING="..." \
  api-fastapi:latest

# 3. Push para Azure Container Registry
az acr login --name seu-registro

docker tag api-fastapi:latest seu-registro.azurecr.io/api-fastapi:latest
docker push seu-registro.azurecr.io/api-fastapi:latest

# 4. Deploy para Container Instances
az container create \
  --resource-group myResourceGroup \
  --name api-fastapi-kauane \
  --image seu-registro.azurecr.io/api-fastapi:latest \
  --ports 8000 \
  --environment-variables \
    APPLICATIONINSIGHTS_CONNECTION_STRING="..." \
  --registry-login-server seu-registro.azurecr.io \
  --registry-username seu-usuario \
  --registry-password sua-senha
```

---

## Configurações Pós-Deploy

### 1. Configurar Variáveis de Ambiente

```bash
# Via Azure CLI
az webapp config appsettings set \
  -g myResourceGroup \
  -n api-fastapi-kauane \
  --settings \
    "APPLICATIONINSIGHTS_CONNECTION_STRING=InstrumentationKey=..." \
    "PYTHONPATH=/home/site/wwwroot" \
    "SCM_DO_BUILD_DURING_DEPLOYMENT=true"

# Ou via Portal
Azure Portal > App Service > Settings > Configuration
```

### 2. Configurar Banco de Dados

```bash
# 1. Firewall do Azure SQL
az sql server firewall-rule create \
  -g myResourceGroup \
  -s dbapidevops \
  -n AllowAppService \
  --start-ip-address 0.0.0.0 \
  --end-ip-address 255.255.255.255

# 2. Testar conexão
sqlcmd -S dbapidevops.database.windows.net \
       -U usuario \
       -P senha \
       -d dbapidevops
```

### 3. Configurar Application Insights

```bash
# 1. Criar Application Insights
az monitor app-insights component create \
  --resource-group myResourceGroup \
  --app api-fastapi-kauane \
  --location canadacentral \
  --application-type web

# 2. Obter Connection String
az monitor app-insights component show \
  --resource-group myResourceGroup \
  --app api-fastapi-kauane \
  --query connectionString

# 3. Adicionar ao App Service
az webapp config appsettings set \
  -g myResourceGroup \
  -n api-fastapi-kauane \
  --settings "APPLICATIONINSIGHTS_CONNECTION_STRING=..."
```

### 4. Configurar Health Checks

```bash
# Via CLI
az webapp config set \
  -g myResourceGroup \
  -n api-fastapi-kauane \
  --generic-configurations '{"healthCheckPath":"/health"}'

# Ou via Portal
Azure > App Service > Settings > General > Health check
```

### 5. Configurar Auto-scaling

```bash
# Criar regra de auto-scale
az monitor autoscale create \
  --resource-group myResourceGroup \
  --resource-name api-fastapi-kauane \
  --resource-type "Microsoft.Web/serverfarms" \
  --min-count 1 \
  --max-count 3 \
  --count 1

# Adicionar regra (scale up quando CPU > 80%)
az monitor autoscale rule create \
  --resource-group myResourceGroup \
  --autoscale-name api-scale \
  --condition "Percentage CPU > 80 avg 5m" \
  --scale out 1
```

### 6. Configurar HTTPS

```bash
# Azure gerencia certificados automaticamente
# HTTPS já está ativado por padrão

# Forçar HTTPS
az webapp update \
  -g myResourceGroup \
  -n api-fastapi-kauane \
  --https-only true
```

---

## Monitoramento do Deploy

### Checklist Pós-Deploy

```
✅ API está respondendo?
   curl https://api-fastapi-kauane.azurewebsites.net/health

✅ Endpoints funcionam?
   GET /
   GET /health
   GET /users
   POST /users

✅ Banco de dados conectado?
   curl https://api-fastapi-kauane.azurewebsites.net/users

✅ Logs aparecem?
   Azure Portal > Application Insights > Logs > traces

✅ Performance aceitável?
   Average response time < 500ms

✅ Zero erros?
   Error rate = 0%

✅ Health check OK?
   Status = 200, resposta = {"status":"ok"}
```

### Métricas para Acompanhar

```
1️⃣ Uptime
   Target: 99.9% (máximo 43 minutos de downtime/mês)

2️⃣ Latência
   Target: < 500ms P95

3️⃣ Taxa de Erro
   Target: < 1%

4️⃣ CPU Usage
   Target: < 70% (médio)

5️⃣ Memory Usage
   Target: < 80% (máximo)

6️⃣ Throughput
   Target: > 100 requests/seg
```

### Dashboards Importantes

```
Azure Portal > App Service > Monitoring
```

Visualizar:

- HTTP 4xx/5xx errors
- Average response time
- Requests per second
- CPU & Memory usage
- File system usage

### Logs de Deployment

```bash
# Ver logs em tempo real
az webapp log tail \
  -g myResourceGroup \
  -n api-fastapi-kauane

# Ver histórico
az webapp log download \
  -g myResourceGroup \
  -n api-fastapi-kauane \
  -d logs-folder
```

---

## Rollback (Desfazer Deploy)

### Se Algo Deu Errado

```bash
# 1. Verificar histórico de deployment
az webapp deployment list \
  -g myResourceGroup \
  -n api-fastapi-kauane

# 2. Encontrar versão anterior
# Procurar por status "Success"

# 3. Redeploy versão anterior
az webapp deployment slot swap \
  -g myResourceGroup \
  -n api-fastapi-kauane \
  -s staging

# Ou via GitHub, fazer revert:
git revert <commit-hash>
git push origin main
```

---

## Troubleshooting

### Erro: "Credentials not provided"

```bash
# Solução: Fazer login novamente
az login

# Ou especificar subscription
az login --subscription "SUBSCRIPTION_ID"
```

### Erro: "Application Insights not found"

```bash
# Solução: Verificar connection string
az monitor app-insights component show \
  -g myResourceGroup \
  -a api-fastapi-kauane

# Atualizar em Configuration
az webapp config appsettings set \
  -g myResourceGroup \
  -n api-fastapi-kauane \
  --settings "APPLICATIONINSIGHTS_CONNECTION_STRING=..."
```

### Erro: "Health check failing"

```bash
# Solução: Verificar endpoint /health
curl https://api-fastapi-kauane.azurewebsites.net/health

# Se retornar 5xx, verificar logs
az webapp log tail -g myResourceGroup -n api-fastapi-kauane

# Desativar health check temporariamente
az webapp config set \
  -g myResourceGroup \
  -n api-fastapi-kauane \
  --generic-configurations '{"healthCheckPath":""}'
```

### Erro: "Slow deployment"

```bash
# Verificar se está compilando Python
# Azure tenta fazer pip install durante deploy

# Solução: Usar SCM_DO_BUILD_DURING_DEPLOYMENT
az webapp config appsettings set \
  -g myResourceGroup \
  -n api-fastapi-kauane \
  --settings "SCM_DO_BUILD_DURING_DEPLOYMENT=true"
```

---

## Automatização com Scripts

### Script: Deploy Automático

```bash
#!/bin/bash
# deploy.sh

echo "🚀 Iniciando deploy..."

# 1. Setup
RESOURCE_GROUP="myResourceGroup"
APP_NAME="api-fastapi-kauane"

# 2. Build
echo "📦 Building..."
pip install -r requirements.txt

# 3. Login
echo "🔐 Fazendo login..."
az login

# 4. Deploy
echo "🚀 Deploying..."
az webapp up \
  --resource-group $RESOURCE_GROUP \
  --name $APP_NAME \
  --runtime "PYTHON:3.10"

# 5. Verificar
echo "✅ Verificando..."
curl https://${APP_NAME}.azurewebsites.net/health

echo "✅ Deploy concluído!"
```

### Script: Monitorar Deploy

```bash
#!/bin/bash
# monitor.sh

RESOURCE_GROUP="myResourceGroup"
APP_NAME="api-fastapi-kauane"

echo "📊 Monitorando aplicação..."

# Health check
HEALTH=$(curl -s https://${APP_NAME}.azurewebsites.net/health)
echo "Health: $HEALTH"

# Logs
echo ""
echo "📋 Logs recentes:"
az webapp log tail \
  -g $RESOURCE_GROUP \
  -n $APP_NAME \
  --max-lines 10
```

---

## Boas Práticas

✅ **Faça**:

- Deploy automático via GitHub Actions
- Testar localmente antes de push
- Usar staging slots antes de produção
- Monitorar aplicação após deploy
- Manter histórico de versões
- Fazer rollback se preciso
- Documentar changes no commit

❌ **Evite**:

- Deploy manual em produção
- Push sem testes
- Ignorar alertas depois do deploy
- Deletar recursos sem backup
- Modificar config via Portal
- Usar mesma database para dev/prod
- Deploy durante horário de pico

---

## Recursos

- [Azure Web App Docs](https://learn.microsoft.com/en-us/azure/app-service/overview)
- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [Azure CLI Reference](https://learn.microsoft.com/en-us/cli/azure/reference-index)
