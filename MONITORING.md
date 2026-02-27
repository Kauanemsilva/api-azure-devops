# 📊 Guia de Monitoramento & Observabilidade

## Índice

1. [Overview](#overview)
2. [Application Insights](#application-insights)
3. [Azure Monitor](#azure-monitor)
4. [Dashboards](#dashboards)
5. [Alertas](#alertas)
6. [Queries KQL](#queries-kql)
7. [Troubleshooting](#troubleshooting)

---

## Overview

### Arquitetura de Observabilidade

```
Aplicação Python
    ↓ logs, traces, metrics
Application Insights (Ingestão)
    ↓
Azure Monitor (Armazenamento & Análise)
    ↓
Dashboards, Alertas, Reports
```

### Componentes Monitorados

| Componente        | Ferramenta           | Frequência |
| ----------------- | -------------------- | ---------- |
| **Logs**          | Application Insights | Real-time  |
| **Traces**        | OpenTelemetry        | Real-time  |
| **Métricas**      | Application Insights | 1 min      |
| **Alertas**       | Azure Monitor        | 1-5 min    |
| **Health Checks** | Azure App Service    | 1 min      |

---

## Application Insights

### Configuração

```python
from azure.monitor.opentelemetry import configure_azure_monitor
import os

connection_string = os.environ.get("APPLICATIONINSIGHTS_CONNECTION_STRING")

if connection_string:
    configure_azure_monitor(connection_string=connection_string)
    print("✓ Azure Monitor configurado")
```

### O que é Rastreado Automaticamente

**Dados de Request**:

```
- URL acessada
- Método HTTP (GET, POST, etc)
- Status code
- Duração da requisição
- IP do cliente
- User agent
```

**Dados de Response**:

```
- Tempo de resposta
- Tamanho do payload
- Headers
- Erros/Exceções
```

**Logs Estruturados**:

```python
import logging

logger = logging.getLogger(__name__)

@app.get("/users")
def get_users():
    logger.info("📋 Listando usuários")  # INFO
    logger.warning("⚠️ Consulta lenta")   # WARNING
    logger.error("❌ Erro ao buscar")     # ERROR
```

### Dados Disponíveis

**No painel de Trace**:

- Timestamp exato
- Mensagem de log
- Nível (INFO, WARNING, ERROR)
- Severidade
- Contexto de execução

---

## Azure Monitor

### Painel de Monitoramento

**Acesso**: Azure Portal > Monitor > Visão Geral

**Métricas Padrão**:

```
CPU Usage (%)
Memory Usage (%)
Request Count (por segundo)
Response Time (ms)
Error Rate (%)
Disk I/O (ops/seg)
```

### Live Metrics (Tempo Real)

**Acesso**: Application Insights > Live Metrics Stream

**Mostra em tempo real**:

```
Requisições chegando ▶▶▶
Tempo de resposta (ms)
Taxa de sucesso/erro
Servidores ativos
Performance instantânea
```

### Performance Counters

```
Processador
- % CPU Time
- % User Time
- % Privileged Time

Memória
- Available Bytes
- Pages/sec
- % Committed Bytes In Use

Rede
- Bytes Received/sec
- Bytes Sent/sec
```

---

## Dashboards

### Criar Dashboard Personalizado

1. **Azure Portal** > Dashboard > Criar novo
2. **Add** + Adicionar tiles
3. **Selecionar** Application Insights como fonte
4. **Configurar** métricas desejadas

### Dashboard Recomendado

```
┌────────────────────────────────────────────────┐
│           API Health Dashboard                 │
├────────────────────────────────────────────────┤
│                                                │
│  ┌──────────────┐  ┌──────────────┐           │
│  │ Requests/sec │  │ Avg Response │           │
│  │      25      │  │    125 ms    │           │
│  └──────────────┘  └──────────────┘           │
│                                                │
│  ┌──────────────┐  ┌──────────────┐           │
│  │ Error Rate   │  │  Availability│           │
│  │    1.2%      │  │    99.8%     │           │
│  └──────────────┘  └──────────────┘           │
│                                                │
│  ┌────────────────────────────────────────┐   │
│  │ CPU Usage (%)        - 45%             │   │
│  │ Memory Usage (%)     - 62%             │   │
│  │ Disk I/O (ops/sec)   - 128            │   │
│  └────────────────────────────────────────┘   │
│                                                │
│  ┌────────────────────────────────────────┐   │
│  │ Recent Errors (últimas 24h)            │   │
│  │ • TypeError in line 45 (1 ocorrência)  │   │
│  │ • ConnectionError (3 ocorrências)      │   │
│  └────────────────────────────────────────┘   │
│                                                │
└────────────────────────────────────────────────┘
```

---

## Alertas

### Tipos de Alertas Configurados

#### 1. High CPU Usage

```
Condition: CPU > 80%
Duration: 5 minutos
Severity: Warning
Action: Email notification
```

**Verificar em**:

```
Azure Portal > Monitor > Alerts > Alert Rules
Search for "High CPU"
```

#### 2. High Memory Usage

```
Condition: Memory > 90%
Duration: 5 minutos
Severity: Critical
Action: Email + SMS
```

#### 3. High Error Rate

```
Condition: (Failed requests / Total requests) > 5%
Duration: 1 minuto
Severity: Critical
Action: Email + PagerDuty
```

#### 4. Slow Response Time

```
Condition: P95 Response Time > 1000ms
Duration: 5 minutos
Severity: Warning
Action: Email
```

### Criar Nova Regra de Alerta

1. **Azure Portal** > Monitor > Alerts > New Alert Rule
2. **Selecionar** Escopo (Application Insights)
3. **Configurar** Condição (métrica, operador, limite)
4. **Definir** Ação (notification, action group)
5. **Salvar** Alerta

**Exemplo KQL**:

```kusto
requests
| where duration > 1000
| summarize count() by bin(timestamp, 5m)
| where count_ > 10
```

### Histórico de Alertas

```
Azure Portal > Monitor > Alerts > Alert History
```

Ver:

- Quando dispararou
- Severity
- Recurso afetado
- Status

---

## Queries KQL

### Básicas

#### Todos os logs das últimas 24h

```kusto
traces
| order by timestamp desc
| limit 100
```

#### Filtrar por severidade

```kusto
traces
| where severity == "Error"
| order by timestamp desc
```

#### Contar por tipo

```kusto
traces
| summarize count() by severity
```

### Performance

#### Requisições lentas (P95 > 500ms)

```kusto
requests
| where duration > 500
| summarize
    count = count(),
    avg_duration = avg(duration),
    p95_duration = percentile(duration, 95)
  by tostring(url)
```

#### Taxa de erro por hora

```kusto
requests
| summarize
    total = count(),
    failed = toscalar(countif(success == false))
  by bin(timestamp, 1h)
| extend error_rate = (failed * 100.0) / total
| order by timestamp desc
```

#### Endpoint mais acessado

```kusto
requests
| summarize
    calls = count(),
    avg_time = avg(duration)
  by tostring(url)
| order by calls desc
| limit 10
```

### Análise

#### Buscar exceções

```kusto
exceptions
| where type == "System.Exception"
| summarize count() by exceptionType
| order by count_ desc
```

#### Timeline de eventos

```kusto
traces
| union requests | union exceptions
| order by timestamp desc
| project timestamp, type, name
```

#### Distribuição de resposta por status

```kusto
requests
| summarize count() by tostring(resultCode)
| project resultCode, count_
```

### Custom Queries

#### Eventos de audit

```kusto
customEvents
| where name == "UserCreated"
| project timestamp, user_id = tostring(customDimensions.user_id)
| order by timestamp desc
```

#### Rastrear user journey

```kusto
requests
| where client_Browser == "Chrome"
| where timestamp > ago(1d)
| summarize
    page_views = count(),
    avg_duration = avg(duration)
  by session_Id
| order by page_views desc
```

---

## Troubleshooting

### Problema: Logs não aparecem no Application Insights

**Causas Possíveis**:

1. `APPLICATIONINSIGHTS_CONNECTION_STRING` não configurada
2. Connection string inválida
3. Aplicação não foi reiniciada após mudar .env
4. Firewall bloqueando conexão

**Solução**:

```bash
# 1. Verificar .env
cat .env | grep APPLICATIONINSIGHTS

# 2. Validar connection string
# Deve conter: InstrumentationKey=..., IngestionEndpoint=...

# 3. Reiniciar aplicação
# Parar servidor (CTRL+C)
# Iniciar novamente: python -m uvicorn main:app --reload

# 4. Fazer requisição de teste
curl http://localhost:8000/health

# 5. Aguardar 30-60 segundos
# Application Insights leva tempo para sincronizar

# 6. Verificar no portal
# Azure Portal > Application Insights > Logs > traces
```

### Problema: Alertas não disparando

**Causas Possíveis**:

1. Regra desabilitada
2. Métrica não está sendo coletada
3. Limite muito alto
4. Action Group não configurada

**Solução**:

```bash
# 1. Verificar se alerta está habilitado
Azure Portal > Monitor > Alerts > Alert Rules
# Status deve ser "Enabled"

# 2. Testar métrica
# Forçar CPU alta por 5+ minutos

# 3. Checar Action Group
Azure Portal > Monitor > Action Groups
# Verificar endereço de email

# 4. Ver history de alertas
Azure Portal > Monitor > Alerts > Alert History
```

### Problema: High costs no Application Insights

**Causa**: Muitos dados sendo ingestados

**Solução**:

```python
# 1. Configurar sampling (reduz volume)
from azure.monitor.opentelemetry import configure_azure_monitor

configure_azure_monitor(
    connection_string=os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING"),
    sampling_ratio=0.5,  # 50% dos dados
)

# 2. Limpar dados antigos
# Azure Portal > Application Insights > Retention
# Reduzir de 90 para 30 dias
```

### Problema: Queries KQL são lenta

**Solução**:

```kusto
// ❌ Lento
traces
| where timestamp > ago(90d)  // Toda a retenção
| search "error"

// ✅ Rápido
traces
| where timestamp > ago(7d)   // Últimos 7 dias
| where severity == "Error"   // Filtro específico
| limit 1000
```

### Debug: Verificar configuração

```python
import os
from azure.monitor.opentelemetry import configure_azure_monitor

connection_string = os.environ.get("APPLICATIONINSIGHTS_CONNECTION_STRING")

print(f"Connection String: {connection_string}")
print(f"Válida: {connection_string and 'InstrumentationKey=' in connection_string}")

try:
    configure_azure_monitor(connection_string=connection_string)
    print("✓ Azure Monitor configurado com sucesso")
except Exception as e:
    print(f"❌ Erro: {e}")
```

---

## Relatórios Automáticos

### Relatório de Performance

```
Azure Portal > Application Insights > Performance

Mostra:
- Operações mais lentas
- Dependências externas
- Gargalos
- Recomendações
```

### Relatório de Confiabilidade

```
Azure Portal > Application Insights > Failures

Mostra:
- Taxa de falha
- Tipos de erro
- Stack traces
- Impacto do usuário
```

### Relatório de Uso

```
Azure Portal > Application Insights > Usage

Mostra:
- Usuários únicos
- Sessões
- Page views
- Eventos customizados
```

---

## Melhores Práticas

✅ **Faça**:

- Logar eventos importantes
- Usar níveis de severidade (!INFO, WARNING, ERROR)
- Adicionar contexto aos logs
- Monitorar continuamente
- Testar alertas mensalmente

❌ **Evite**:

- Logar informações sensíveis (senhas, tokens)
- Logar a cada microsegundo (impact performance)
- Ignorar alertas
- Deixar alertas sem configuração
- Usar queries muito pesadas

---

## Recursos Adicionais

- [Application Insights Docs](https://learn.microsoft.com/en-us/azure/azure-monitor/app/app-insights-overview)
- [KQL Documentation](https://learn.microsoft.com/en-us/kusto/query/)
- [Azure Monitor Alerts](https://learn.microsoft.com/en-us/azure/azure-monitor/alerts/alerts-overview)
