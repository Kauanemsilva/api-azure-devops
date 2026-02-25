# 🏗️ Arquitetura - Cloud & DevOps

## Pipeline CI/CD Completa

```
┌─────────────────────────────────────────────────────────────────┐
│                     Developer Workflow                           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                      git push origin main
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    GitHub Repository                             │
│  - Versionamento do código                                      │
│  - Pull Requests & Code Review                                  │
│  - Triggers automáticos                                         │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│               GitHub Actions Workflow                            │
│  ┌────────────────────────────────────────────────────────┐    │
│  │ 1. Checkout do código                                 │    │
│  │ 2. Setup Python 3.9                                   │    │
│  │ 3. Instalar dependências (pip install -r req.txt)    │    │
│  │ 4. Lint & Tests (pytest)                             │    │
│  │ 5. Preparar release                                   │    │
│  └────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│            Azure Web App Deployment                              │
│  📦 Package da aplicação                                         │
│  ┌────────────────────────────────────────────────────────┐    │
│  │ Azure App Service                                     │    │
│  │ - Runtime: Python 3.9                                 │    │
│  │ - HTTP Server: uvicorn                                │    │
│  │ - Auto-restart: Enabled                               │    │
│  │ - Health checks: Ativadas                             │    │
│  └────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ✅ API Online & Rodando
        https://api-azure-devops-seu-nome.azurewebsites.net
```

---

## 📊 Fluxo de Deploy Automático

```
Local Development              GitHub             Azure
      │                          │                  │
      │ git push                 │                  │
      ├────────────────────────►  │                  │
      │                          │ GitHub Actions   │
      │                          ├────────────────►  │
      │                          │  Teste & Build    │
      │                          │  Deploy Code      │
      │                          ├────────────────►  │
      │                          │                App Running
      │  Acessa API online ◄─────┼──────────────────┤
      │                          │                  │
```

---

## 🔐 Segurança & Secrets

```
GitHub Secrets (Protegido)
├── AZURE_APP_NAME
│   └── Nome da aplicação na Azure
└── AZURE_PUBLISH_PROFILE
    └── Credenciais de deploy (Publish Profile)

❌ Nunca commitar secrets no código!
✅ Usar GitHub Secrets conforme demonstrado
```

---

## 🏢 Estrutura do Projeto

```
api-azure-devops/
│
├── app/                        # Aplicação Principal
│   ├── __init__.py
│   ├── main.py                # Entrada da aplicação
│   ├── models/                # Modelos de dados
│   │   ├── __init__.py
│   │   └── user.py
│   └── routes/                # Endpoints/Rotas
│       ├── __init__.py
│       └── users.py
│
├── .github/
│   └── workflows/
│       └── deploy.yml         # Pipeline CI/CD (GitHub Actions)
│
├── requirements.txt           # Dependências Python
├── README.md                  # Documentação completa
├── SETUP.md                   # Guia de configuração
├── web.config                 # Configuração Azure (Python)
├── .gitignore                 # Git ignore
├── .env.example               # Variáveis de ambiente (exemplo)
├── test_main.py               # Testes unitários
│
└── venv/                      # Virtual Environment (não commitar)
```

---

## 🚀 Fluxo de Desenvolvimento Recomendado

### 1. Feature Development

```bash
git checkout -b feature/nova-endpoint
# ... fazer alterações ...
git add .
git commit -m "Adiciona nova endpoint"
```

### 2. Code Review & Testing

```bash
git push origin feature/nova-endpoint
# Criar Pull Request no GitHub
# Aguardar aprovação
```

### 3. Merge & Auto Deploy

```bash
# Merge na branch main (via GitHub ou local)
git checkout main
git merge feature/nova-endpoint
git push origin main

# 🎯 GitHub Actions automaticamente:
#    ✅ Executa testes
#    ✅ Valida código
#    ✅ Faz build
#    ✅ Deploy na Azure
#    ✅ Health checks
```

---

## 📈 Escalabilidade Futura

```
Atual (MVP)
├── App Service (B1)
├── Banco fake em memória
└── Autenticação: Nenhuma

Próximos Passos
├── Database PostgreSQL
├── Redis Cache
├── API Gateway
├── Authentication (JWT)
├── Rate Limiting
└── Monitoring & Logging (Azure Monitor)

Enterprise
├── Kubernetes (AKS)
├── CI/CD avançada
├── Disaster Recovery
├── Multi-region
└── GitOps (ArgoCD)
```

---

## 🔍 Logs & Monitoring

### Ver Logs da Aplicação

```bash
az webapp log tail \
  --resource-group myResourceGroup \
  --name api-azure-devops-seu-nome
```

### Análise de Performance

```bash
# Azure Portal > App Service > Metrics
# - CPU Usage
# - Memory Usage
# - HTTP 5xx errors
# - Response time
```

### GitHub Actions Logs

```
GitHub > Actions > [Workflow] > [Run] > Logs
```

---

## ✅ Checklist de Deploy

- [ ] Código testado localmente
- [ ] Tests passando (`pytest`)
- [ ] Dependências atualizadas (`requirements.txt`)
- [ ] Secrets configurados no GitHub
- [ ] Web.config presente no root
- [ ] README atualizado
- [ ] Branch main está pronta
- [ ] GitHub Actions workflow criado
- [ ] Azure App Service ativa
- [ ] Health check respondendo

Após completar: **git push origin main** 🚀

---

## 🆘 Troubleshooting

### Problema: Deploy falha

**Solução**: Verificar logs do GitHub Actions e Azure

### Problema: API não responde

**Solução**: Reiniciar App Service via Azure Portal

### Problema: Secrets expirados

**Solução**: Gerar novo Publish Profile e atualizar no GitHub

### Problema: Testes falhando

**Solução**: Executar localmente `pytest` e corrigir erros

---

## 📚 Recursos

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [GitHub Actions Docs](https://docs.github.com/actions)
- [Azure App Service Python](https://docs.microsoft.com/azure/app-service/quickstart-python)
- [Pydantic Docs](https://docs.pydantic.dev/)
- [Uvicorn Docs](https://www.uvicorn.org/)

---

**Desenvolvido para demonstrar expertise em Cloud & DevOps** ☁️🚀
