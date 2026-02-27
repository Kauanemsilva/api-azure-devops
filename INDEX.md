# 📚 Índice de Documentação - API Azure DevOps

> Navegação centralizada para toda a documentação do projeto

---

## 🚀 Comece Aqui

### Novo no Projeto?

1. Leia **[README.md](./README.md)** - Visão geral e quick start
2. Consulte **[SETUP.md](./SETUP.md)** - Configuração local
3. Explore os endpoints em **[http://localhost:8000/docs](http://localhost:8000/docs)**

### Quer Fazer Deploy?

1. Veja **[DEPLOYMENT.md](./DEPLOYMENT.md)** - Guia completo de deployment
2. Acompanhe em **GitHub Actions** - Deploy automático
3. Monitore em **[MONITORING.md](./MONITORING.md)** - Observabilidade

### Algo Não Funciona?

1. Consulte **[TROUBLESHOOTING.md](./TROUBLESHOOTING.md)** - Problemas comuns
2. Procure por sua função específica
3. Siga as soluções passo a passo

---

## 📖 Documentação Completa

### 1. **README.md**

**Para**: Todos os desenvolvedores, stakeholders, portfolios

**Contém**:

- ✅ Visão geral do projeto
- ✅ Status atual (production-ready)
- ✅ Stack tecnológico
- ✅ Quick start local (5 min)
- ✅ Endpoints e exemplos
- ✅ Pipeline CI/CD
- ✅ Links importantes

**Quando ler**:

- Primeira vez usando o projeto
- Para apresentar ao chefe/cliente
- Para portfolio em GitHub

---

### 2. **SETUP.md**

**Para**: Desenvolvedores (com foco em setup local)

**Contém**:

- ✅ Pré-requisitos
- ✅ Clone & instalação
- ✅ Variáveis de ambiente
- ✅ Execução local
- ✅ Testes básicos
- ✅ Troubleshooting inicial

**Quando ler**:

- Primeira vez configurando o projeto
- Quando novo dev entra no time
- Antes de começar a desenvolver

---

### 3. **ARCHITECTURE.md**

**Para**: Tech leads, arquitetos, DevOps

**Contém**:

- ✅ Diagrama de arquitetura
- ✅ Fluxo de deploy
- ✅ Estrutura de pastas
- ✅ Decisões arquiteturais
- ✅ Componentes do sistema
- ✅ Fluxo de dados

**Quando ler**:

- Para entender design do sistema
- Antes de fazer mudanças estruturais
- Para integrar com outros serviços

---

### 4. **DOCUMENTATION.md** ⭐ PRINCIPAL

**Para**: Desenvolvedores que querem entender tudo

**Contém**:

- ✅ Overview completo
- ✅ Arquitetura técnica (com diagramas)
- ✅ Componentes em detalhe
- ✅ Stack tecnológico (versões)
- ✅ **Todos os endpoints** (4 endpoints)
- ✅ Banco de dados (schema, operações)
- ✅ Observabilidade
- ✅ Segurança

**Quando ler**:

- Para referência técnica completa
- Quando precisa entender um componente
- Para onboarding de novo dev

---

### 5. **DEPLOYMENT.md**

**Para**: DevOps, SRE, desenvolvedores

**Contém**:

- ✅ Opções de deploy (3 formas)
- ✅ **GitHub Actions (automático)** ✨
- ✅ Azure CLI (manual)
- ✅ Docker (avançado)
- ✅ Configurações pós-deploy
- ✅ Monitoramento de deploy
- ✅ Rollback
- ✅ Scripts de automação

**Quando ler**:

- Antes de fazer primeiro deploy
- Para setup de CI/CD
- Para troubleshoot deployment issues
- Para automação

---

### 6. **MONITORING.md**

**Para**: DevOps, SRE, operations

**Contém**:

- ✅ Arquitetura observabilidade
- ✅ Application Insights (detalhado)
- ✅ Azure Monitor (alertas)
- ✅ Dashboards (criar custom)
- ✅ **Queries KQL** (12+ exemplos)
- ✅ Live metrics
- ✅ Troubleshooting observabilidade

**Quando ler**:

- Para configurar monitoramento
- Quando precisa fazer queries de logs
- Para criar alertas
- Para investigar problemas

---

### 7. **TROUBLESHOOTING.md**

**Para**: Todos (quando algo quebra)

**Contém**:

- ✅ 40+ problemas comuns
- ✅ Sintomas + Causas + Soluções
- ✅ Erros de inicialização
- ✅ Erros de banco de dados
- ✅ Problemas de performance
- ✅ Erros de deployment
- ✅ Checklist de debug

**Quando ler**:

- **PRIMEIRO** quando algo não funciona!
- Para aprender a debugar
- Para referência rápida

---

## 🎯 Fluxos de Trabalho

### Fluxo: Setup Local Inicial

```
1. README.md (visão geral)
   ↓
2. SETUP.md (configurar)
   ↓
3. Executar: python -m uvicorn main:app --reload
   ↓
4. Testar: curl http://localhost:8000/health
   ↓
5. DOCUMENTATION.md (entender endpoints)
```

### Fluxo: Primeiro Deployment

```
1. README.md (entender projeto)
   ↓
2. DEPLOYMENT.md > "Deploy Automático"
   ↓
3. Configurar GitHub Secrets
   ↓
4. git push → GitHub Actions dispara
   ↓
5. MONITORING.md (verificar)
   ↓
6. TROUBLESHOOTING.md (se erro)
```

### Fluxo: Investigar Bug/Performance

```
1. TROUBLESHOOTING.md (procurar sintoma)
   ↓
2. Seguir solução
   ↓
3. Se data/logs → MONITORING.md
   ↓
4. Se banco → DOCUMENTATION.md (seção Database)
   ↓
5. Se deploy → DEPLOYMENT.md
```

### Fluxo: Criar Query de Logs

```
1. MONITORING.md > "Queries KQL"
   ↓
2. Copiar exemplo relevante
   ↓
3. Adaptar para seu caso
   ↓
4. Azure Portal > Application Insights > Logs
   ↓
5. Colar e executar
```

---

## 🏃 Atalhos Rápidos

### Por Tarefa

| Tarefa              | Arquivo            | Seção                |
| ------------------- | ------------------ | -------------------- |
| Instalar localmente | SETUP.md           | Pré-requisitos       |
| Entender endpoints  | DOCUMENTATION.md   | Endpoints            |
| Fazer deploy        | DEPLOYMENT.md      | Deploy Automático    |
| Ver logs            | MONITORING.md      | Application Insights |
| Query de dados      | MONITORING.md      | Queries KQL          |
| API está lenta      | TROUBLESHOOTING.md | Performance          |
| Deploy falhando     | TROUBLESHOOTING.md | Erros Deployment     |
| Criar alerta        | MONITORING.md      | Alertas              |
| Banco de dados      | DOCUMENTATION.md   | Banco de Dados       |
| Segurança           | DOCUMENTATION.md   | Segurança            |

### Por Função

| Função                 | Documentação Essencial                           |
| ---------------------- | ------------------------------------------------ |
| **Dev Python/FastAPI** | README → SETUP → DOCUMENTATION                   |
| **DevOps/SRE**         | DEPLOYMENT → MONITORING → TROUBLESHOOTING        |
| **Tech Lead**          | ARCHITECTURE → DOCUMENTATION → DEPLOYMENT        |
| **Novo no Projeto**    | README → SETUP → TROUBLESHOOTING → DOCUMENTATION |
| **Em Produção**        | MONITORING → TROUBLESHOOTING                     |

---

## 📊 Estrutura de Documentação

```
.
├── README.md                    # 📌 Comece aqui!
├── DOCUMENTATION.md             # 🔍 Referência técnica completa
├── SETUP.md                     # 🔧 Setup inicial
├── ARCHITECTURE.md              # 🏗️ Design do sistema
├── DEPLOYMENT.md                # 🚀 Deploy & CI/CD
├── MONITORING.md                # 📊 Observabilidade & Logs
├── TROUBLESHOOTING.md           # 🔧 Problemas & Soluções
└── INDEX.md (este arquivo)      # 📚 Índice de navegação
```

---

## 🌐 Referências Externas

### Documentação Oficial

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [SQLAlchemy Docs](https://docs.sqlalchemy.org/)
- [Python 3.10 Docs](https://docs.python.org/3.10/)

### Azure

- [App Service](https://learn.microsoft.com/en-us/azure/app-service/)
- [Application Insights](https://learn.microsoft.com/en-us/azure/azure-monitor/app/app-insights-overview)
- [Azure SQL Database](https://learn.microsoft.com/en-us/azure/azure-sql/database/)
- [Azure Monitor](https://learn.microsoft.com/en-us/azure/azure-monitor/)

### DevOps

- [GitHub Actions](https://docs.github.com/en/actions)
- [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/)
- [KQL (Kusto Query Language)](https://learn.microsoft.com/en-us/kusto/query/)

---

## ✅ Checklist de Documentação

- [x] README.md - Visão geral e quick start
- [x] SETUP.md - Setup local detalhado
- [x] ARCHITECTURE.md - Design do sistema
- [x] DOCUMENTATION.md - Referência técnica completa
- [x] DEPLOYMENT.md - Deploy & CI/CD automático
- [x] MONITORING.md - Observabilidade & queries KQL
- [x] TROUBLESHOOTING.md - 40+ problemas com soluções
- [x] INDEX.md - Este índice de navegação

---

## 🚀 Status Atual

| Componente    | Status                | Docs             |
| ------------- | --------------------- | ---------------- |
| API FastAPI   | ✅ Production         | DOCUMENTATION.md |
| Database      | ✅ Azure SQL + SQLite | DOCUMENTATION.md |
| CI/CD         | ✅ GitHub Actions     | DEPLOYMENT.md    |
| Monitoring    | ✅ App Insights       | MONITORING.md    |
| Startup Setup | ✅ Automated          | SETUP.md         |

---

## 🆘 Precisa de Ajuda?

1. **Erro específico?** → [TROUBLESHOOTING.md](./TROUBLESHOOTING.md)
2. **Não sabe por onde começar?** → [README.md](./README.md)
3. **Quer entender tudo?** → [DOCUMENTATION.md](./DOCUMENTATION.md)
4. **Deploy?** → [DEPLOYMENT.md](./DEPLOYMENT.md)
5. **Logs/Monitoring?** → [MONITORING.md](./MONITORING.md)

---

**Última atualização**: Fevereiro 2026  
**Status**: ✅ Completo e atualizado
