# Guia de Execução da Demo — CA Vida Solvency II
## Duração Total: 1h30min | Plataforma Snowflake

---

## Preparação (5 min antes)

1. Abrir Snowsight: https://app.snowflake.com/sfseeurope/dtinoco_aws/
2. Ter abertos em tabs:
   - **Notebook**: `CAVIDA_DEMO.REGULATORY.CAVIDA_DEMO_V2_EXECUCAO` ← PRINCIPAL (tudo aqui!)
   - **Streamlit App**: `CAVIDA_DEMO.REGULATORY.SLV2_WORKFLOW`
   - **Snowflake Intelligence**: Agent `CA Vida - Solvency II Intelligence`
3. Verificar que warehouses estão activos: `SHOW WAREHOUSES LIKE 'CAVIDA%';`

> **NOTA**: O notebook `CAVIDA_DEMO_V2_EXECUCAO` contém TODOS os scripts SQL, comentários, tabelas comparativas e mensagens para o presenter. Basta executar célula a célula durante a demo. Os scripts SQL avulsos (02_architecture/, 05_security/, etc.) já não são necessários.

---

## Fluxo da Demo

| ACT | Duração | Onde executar | O que mostrar |
|-----|---------|--------------|---------------|
| 1 - Platform | 25 min | **Notebook** (células 2-13) | Warehouses, Clone, Time Travel, dbt |
| 2 - Governance | 20 min | **Notebook** (células 14-27) | Tags, EU, Masking, RLS |
| 3 - Streamlit | 25 min | **Streamlit App** | 16 passos SLV II ao vivo |
| 4 - FinOps | 10 min | **Notebook** (células 30-32) | Monitors, custos, auto-suspend |
| 5 - Intelligence | 10 min | **Snowflake Intelligence** | NLQ em português |

---

## ACT 1: Platform Foundation (25 min)

### 1.1 — Arquitectura Multi-Ambiente (5 min)
**💬 Mensagem**: "Já migrámos o vosso processo SAS para Snowflake. Separação total de compute e storage."

**No Notebook**: Executar células de SHOW WAREHOUSES e SHOW SCHEMAS

**Pontos-chave**:
- 4 warehouses (XS/XS/S/M) para diferentes workloads
- Escalar em 2 segundos (ALTER WAREHOUSE SET SIZE)
- **vs Databricks**: Clusters always-on = custo mesmo inactivos
- **vs BigQuery**: Sem controlo granular de compute por equipa

### 1.2 — Zero-Copy Clone (5 min)
**💬 Mensagem**: "Precisam de ambiente de teste? Instantâneo. Zero bytes extra."

**No Notebook**: Executar CREATE SCHEMA TEST CLONE PROD

**Pontos-chave**:
- < 1 segundo para clonar qualquer volume de dados
- **vs Databricks**: Delta Clone requer compute, leva minutos
- **vs BigQuery**: NÃO EXISTE equivalente

### 1.3 — Time Travel (5 min)
**💬 Mensagem**: "Se alguém apagar dados? Recuperamos em segundos. Sem backup."

**No Notebook**: Executar DELETE → AT(OFFSET) → INSERT restore

**Pontos-chave**:
- 90 dias automáticos (Business Critical)
- UNDROP para recuperar objectos eliminados
- **vs Databricks**: Delta versioning = gestão manual, VACUUM
- **vs BigQuery**: Apenas 7 dias, sem UNDROP

### 1.4 — dbt Project (10 min)
**💬 Mensagem**: "Pipeline versionado, deployed como objecto Snowflake. Tudo auditável."

**Acções**:
1. No Notebook: mostrar objectos criados (célula SELECT de DEV_STAGING/DEV_PROD)
2. Navegar no Snowsight: CAVIDA_DEMO → REGULATORY → dbt Projects → `CAVIDA_SLV2_PROJECT`
3. Mostrar DAG (grafo de dependências): staging → intermediate → marts
4. Mostrar que 10/10 modelos passaram

**Pontos-chave**:
- dbt deployed nativamente no Snowflake (objectos geridos)
- **vs Databricks**: Não tem dbt deploy nativo (requer Jobs API externo)
- **vs BigQuery**: Não tem dbt como objecto nativo (requer Cloud Composer)

---

## ACT 2: Governance & Security (20 min)

### 2.1 — Catálogo & Tags (5 min)
**💬 Mensagem**: "Todos os dados classificados. Zero licenças adicionais."

**No Notebook**: Executar SHOW TAGS + SHOW SEMANTIC DIMENSIONS/METRICS

**Pontos-chave**:
- Tags: DATA_DOMAIN, SENSITIVITY, PII
- Semantic View como glossário de negócio (descrições em PT!)
- **vs SAS**: Information Catalog = licença extra
- **vs Databricks**: Unity Catalog tags (mais recente, menos maduro)

### 2.2 — EU Data Residency (3 min)
**💬 Mensagem**: "Dados NUNCA saem da UE. Frankfurt, Business Critical."

**No Notebook**: Executar SELECT CURRENT_REGION()

**Pontos-chave**:
- AWS EU-Central-1 (Frankfurt)
- AES-256 + Tri-Secret Secure
- SOC2, ISO27001, GDPR

### 2.3 — Dynamic Masking (5 min)
**💬 Mensagem**: "Dados sensíveis mascarados automaticamente. Sem código."

**No Notebook**: Executar query como ACCOUNTADMIN → depois como CAVIDA_ANALYST

**Pontos-chave**:
- ACCOUNTADMIN vê dados reais
- ANALYST vê `***MASKED***`
- Política declarativa, aplicada em TODAS as queries
- **vs Databricks**: Row/column filters Unity Catalog (menos flexível)
- **vs BigQuery**: Policy tags apenas column-level

### 2.4 — Row-Level Security (5 min)
**💬 Mensagem**: "O analista só vê últimos 6 meses. Invisível."

**No Notebook**: Executar GROUP BY reference_date como ADMIN → depois como ANALYST

**Pontos-chave**:
- ANALYST não vê erro — simplesmente vê menos linhas
- Segurança por data de referência (últimos 6 meses)
- **vs SAS**: WHERE clauses manuais em cada programa
- **vs Databricks**: Row filters menos maduros

### 2.5 — Lineage (2 min)
**💬 Mensagem**: "Linhagem completa, da origem ao report."

**No Snowsight**: Abrir dbt project → mostrar grafo
- stg_investment_portfolio → int_asset_reconciliation → mart_economic_balance_sheet

---

## ACT 3: Workflow Solvency II — Streamlit (25 min)

**💬 Mensagem**: "O processo SLV II tal como o conhecem — mas dentro de Snowflake."

### Abrir: Streamlit App `SLV2_WORKFLOW`

| Passo | Nome | O que mostrar | Tempo |
|-------|------|---------------|-------|
| 1 | Período de Referência | Write-back (UPDATE directo!) | 2 min |
| 2 | Importação Carteira | Upload ficheiro + histórico | 2 min |
| 3 | Estado CA Gestl | Status colorido + barra progresso | 1 min |
| 4 | Regras de Validação | Executar 10 regras, ver Aprovado/Falhou | 3 min |
| 5 | Reconciliação Activos | Totais por classe + export Excel | 2 min |
| 6-8 | Risk Agility | Registos vazios, ficheiros, passivos | 3 min |
| 9-11 | Download/Import RA | Ficheiros + status | 2 min |
| 12 | Tagetik | Pré-requisitos + carregamento | 2 min |
| 13 | Capital Disponível | Métricas por Tier (M€) | 2 min |
| 14 | Balanço Económico | Variações + delta indicator | 2 min |
| 15 | Fecho Report | Botão de fecho | 1 min |
| 16 | Download Tagetik | Ficheiros finais | 1 min |

**Ponto-chave final**: "16 passos, tudo dentro de Snowflake. Zero infra externa."
- **vs SAS**: SAS Visual Analytics = licença extra, servidores dedicados
- **vs Databricks**: NÃO TEM framework de web apps nativo
- **vs BigQuery**: NÃO TEM framework de web apps nativo

---

## ACT 4: FinOps & Cost Intelligence (10 min)

**💬 Mensagem**: "Controlo total de custos. Impossível no SAS."

### No Notebook: Executar células 30-32

| Demo | O que mostrar |
|------|---------------|
| Resource Monitors | 3 monitors (DEV 100cr, ETL 300cr, PROD 500cr) |
| Cost Attribution | Custos por warehouse em EUR |
| Auto-Suspend | Warehouses SUSPENDED = 0€/hora |

**Pontos-chave**:
- Pay-per-second com limites automáticos
- Custo noite/fim-de-semana = ZERO
- **vs SAS**: Licença fixa anual, sem visibilidade de consumo
- **vs Databricks**: DBU caro, clusters always-on por defeito
- **vs BigQuery**: Pay-per-query mas sem resource monitors

---

## ACT 5: WOW Factor — Snowflake Intelligence (10 min)

**💬 Mensagem**: "E agora, o futuro: perguntar aos dados em PORTUGUÊS."

### Abrir: Snowflake Intelligence → Agent `CA Vida - Solvency II Intelligence`

**Perguntas a fazer (ao vivo!)**:
1. "Qual é o valor total da carteira de investimentos?"
2. "Mostra o balanço económico por tipo de activo"
3. "Qual é o capital disponível por tier?"
4. "Quantos instrumentos temos por classe de activo?"

**Para cada pergunta mostrar**:
- SQL gerado automaticamente
- Resultado formatado
- Visualização (chart) gerada

**Ponto-chave KILLER**: "Isto NÃO EXISTE no SAS. NÃO EXISTE no Databricks. NÃO EXISTE no BigQuery. É EXCLUSIVO Snowflake."

---

## Encerramento (5 min)

### Resumo (mostrar última célula do Notebook)
- 20/20 requisitos demonstrados ✅
- Substituição completa do SAS 9.4
- Sem licenças adicionais para governance, data quality, ou AI

### Call-to-Action
| # | Acção | Prazo |
|---|-------|-------|
| 1 | Workshop hands-on com equipa técnica | 2 semanas |
| 2 | PoC com dados reais SLV II | 4-6 semanas |
| 3 | Migração piloto de 1 pipeline SAS | 6-8 semanas |
| 4 | Plano de migração completo | 8-12 semanas |

### Entregável
- Relatório detalhado: `RELATORIO_DEMONSTRACAO_CA_VIDA.md` (enviado após sessão)

---

## Notas para o Presenter — Perguntas Difíceis

| Pergunta do Cliente | Resposta |
|---------------------|----------|
| "E se o warehouse ficar lento?" | "Escalam em 2 seg: ALTER WAREHOUSE SET SIZE = LARGE. Sem reiniciar nada." |
| "Como fazem backup?" | "Time Travel 90 dias + Fail-Safe 7 dias + Replication cross-region para DR." |
| "Quanto custa?" | "Pay-per-use. Estimativa no sizing document. Sem licenças fixas." |
| "E a migração SAS?" | "dbt converte lógica SAS para SQL. Existem ferramentas automáticas (SnowConvert)." |
| "Quem mais usa no sector segurador?" | "Generali, AXA, Zurich, Legal&General — todos em produção." |
| "E o Databricks?" | "Sem Streamlit, sem NLQ, sem masking declarativo, sem time-travel 90d, clusters caros." |
| "E o BigQuery?" | "Sem apps web, sem dbt deploy, time-travel 7d, sem zero-copy clone." |
| "A migração demora quanto?" | "Pipeline piloto: 6-8 semanas. Full migration: 6-12 meses dependendo de complexidade." |
| "E se quisermos on-prem?" | "Snowflake é 100% cloud mas com Private Link (VPN), dados nunca expostos à internet." |

---

## Objectos Snowflake da Demo

| Tipo | Objecto | Onde usar |
|------|---------|-----------|
| Notebook | `CAVIDA_DEMO.REGULATORY.CAVIDA_DEMO_V2_EXECUCAO` | ACT 1, 2, 4 |
| Streamlit | `CAVIDA_DEMO.REGULATORY.SLV2_WORKFLOW` | ACT 3 |
| Agent | `CAVIDA_DEMO.SEMANTIC.SLV2_INTELLIGENCE_AGENT` | ACT 5 |
| dbt Project | `CAVIDA_DEMO.REGULATORY.CAVIDA_SLV2_PROJECT` | ACT 1.4 |
| Semantic View | `CAVIDA_DEMO.SEMANTIC.SLV2_ANALYTICS` | ACT 2.1, 5 |

---

*Tempo total: 90 minutos | Margem: 5 min Q&A entre secções*
