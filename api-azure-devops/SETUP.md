# Guia Rápido de Setup

## 1️⃣ Setup Local

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/api-azure-devops.git
cd api-azure-devops

# Crie ambiente virtual
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate no Windows

# Instale dependências
pip install -r requirements.txt

# Execute a API
uvicorn app.main:app --reload
```

Acesse: http://localhost:8000/docs

---

## 2️⃣ Setup GitHub

1. Crie um repositório em https://github.com/new
2. Clone e configure:

```bash
git remote add origin https://github.com/seu-usuario/api-azure-devops.git
git branch -M main
git push -u origin main
```

---

## 3️⃣ Setup Azure

```bash
# Faça login
az login

# Crie grupo de recursos
az group create --name myResourceGroup --location eastus

# Crie plano App Service
az appservice plan create \
  --name myAppServicePlan \
  --resource-group myResourceGroup \
  --sku B1 --is-linux

# Crie Web App
az webapp create \
  --resource-group myResourceGroup \
  --plan myAppServicePlan \
  --name api-azure-devops-seu-nome \
  --runtime "PYTHON|3.9"

# Obtenha o Publish Profile
az webapp deployment list-publishing-profiles \
  --resource-group myResourceGroup \
  --name api-azure-devops-seu-nome \
  --query "[0]" > publishprofile.json
```

---

## 4️⃣ Configurar GitHub Actions

1. Vá para seu repositório GitHub
2. Settings > Secrets and variables > Actions
3. Clique "New repository secret"
4. Adicione:
   - `AZURE_APP_NAME`: Nome da sua app (ex: api-azure-devops-seu-nome)
   - `AZURE_PUBLISH_PROFILE`: Conteúdo do publishprofile.json

---

## 5️⃣ Deploy Automático

Agora é simples! A cada `git push`, o GitHub Actions automaticamente:

```bash
git add .
git commit -m "Update API"
git push origin main
```

✅ GitHub Actions executa testes  
✅ Faz build da aplicação  
✅ Deploy na Azure  
✅ Valida se está online

Acompanhe em: GitHub > Actions > Workflow runs

---

## 🔗 URLs Importantes

- **API**: https://api-azure-devops-seu-nome.azurewebsites.net
- **Documentação**: https://api-azure-devops-seu-nome.azurewebsites.net/docs
- **GitHub**: https://github.com/seu-usuario/api-azure-devops
- **Azure Portal**: https://portal.azure.com

---

## 🐛 Troubleshooting

### Deploy falha na Azure?

```bash
# Ver logs
az webapp log tail --resource-group myResourceGroup --name api-azure-devops-seu-nome
```

### GitHub Actions não funciona?

1. Verifique os Secrets estão corretos
2. Vá para Actions e veja o log de erro
3. Valide que o AZURE_PUBLISH_PROFILE não expirou

### API não responde?

```bash
# Reinicie a app
az webapp restart --resource-group myResourceGroup --name api-azure-devops-seu-nome
```

---

✅ **Pronto! Seu portfólio Cloud/DevOps está online!**
