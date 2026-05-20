# Relatório de Demonstração — Plataforma Snowflake para CA Vida

**Documento**: Relatório Pós-Demonstração  
**Cliente**: CA Vida — Companhia de Seguros de Vida (Grupo Crédito Agrícola)  
**Data**: Maio 2026  
**Elaborado por**: Equipa de Pré-Venda Snowflake  
**Classificação**: Confidencial

---

## 1. Sumário Executivo

A presente demonstração apresentou a plataforma Snowflake como solução de substituição integral do SAS 9.4 M8 actualmente em uso pela CA Vida para o processo de reporting regulatório Solvency II.

Foi demonstrado um projecto end-to-end que abrange:
- **Arquitectura multi-ambiente** (DEV/TEST/PROD) com separação total de compute e storage
- **Pipeline de dados** completo via dbt (staging → intermediate → marts)
- **Aplicação web** replicando os 16 passos do workflow Solvency II em Streamlit
- **Governação de dados** com masking dinâmico, RLS e catalogação
- **Controlo de custos** (resource monitors, budgets, atribuição por warehouse)
- **Inteligência Artificial** com Snowflake Intelligence para consultas em linguagem natural

A demonstração foi realizada na região **AWS EU (Frankfurt)**, garantindo total soberania de dados dentro da União Europeia, numa conta **Business Critical** com encriptação em todas as camadas.

---

## 2. Mapeamento de Requisitos

| ID | Requisito | Capacidade Snowflake | Estado |
|----|-----------|---------------------|--------|
| 3 | Separação compute/storage, ambientes Dev/Test/Prod | Warehouses isolados + Zero-Copy Clone | ✅ Demonstrado |
| 5 | Versionamento, rollback, change management | dbt + Git + Time Travel | ✅ Demonstrado |
| 6 | Versionamento de datasets, time-travel | Time Travel (90 dias), Fail-Safe | ✅ Demonstrado |
| 8 | Integração RDBMS, conectividade segura | Snowpipe, External Stages, PrivateLink | ✅ Demonstrado |
| 9 | Dados não-estruturados, APIs, SFTP | Internal Stages, REST API, PUT/GET | ✅ Demonstrado |
| 10 | Web apps, write-back, workflow automation | Streamlit in Snowflake (16 passos SLV II) | ✅ Demonstrado |
| 13 | Catálogo de dados, glossário, pesquisa | Tags, Semantic Views, Horizon Catalog | ✅ Demonstrado |
| 14 | Linhagem técnica (pipeline + coluna) | dbt lineage + ACCESS_HISTORY | ✅ Demonstrado |
| 16 | Qualidade de dados, monitorização, alertas | Validation rules no workflow + DMFs | ✅ Demonstrado |
| 17 | Residência de dados na UE, soberania | Região AWS EU (Frankfurt), Business Critical | ✅ Demonstrado |
| 21 | Segurança a nível de linha e coluna | Dynamic Masking + Row Access Policies | ✅ Demonstrado |
| 30 | Orquestração (scheduling, dependências) | Tasks + dbt orchestration | ✅ Demonstrado |
| 32 | Ferramentas de desenvolvimento pipelines | dbt Cloud/CLI, Snowflake CLI, IDE | ✅ Demonstrado |
| 34 | Controlo de custos, visibilidade | Resource Monitors (3 monitors configurados) | ✅ Demonstrado |
| 35 | Atribuição de custos, showback/chargeback | Warehouses por equipa + ACCOUNT_USAGE views | ✅ Demonstrado |
| 36 | Optimização de custos, detecção idle | Auto-suspend (60s/120s), auto-resume | ✅ Demonstrado |
| 37 | Camada semântica, métricas de negócio | Semantic View com métricas SLV II | ✅ Demonstrado |
| 42 | Capacidades AI/GenAI | Cortex Agent + LLM integration | ✅ Demonstrado |
| 46 | Natural Language Query (NLQ) | Snowflake Intelligence + Cortex Analyst | ✅ Demonstrado |
| 47 | Adopção no sector segurador | Workflow SLV II real + terminologia PT | ✅ Demonstrado |

**Resultado**: 20/20 requisitos demonstrados com sucesso.

---

## 3. Detalhe por Requisito

### Requisito 3 — Separação Compute/Storage, Ambientes

**Descrição**: A plataforma deve permitir separação total entre computação e armazenamento, com ambientes isolados para desenvolvimento, testes e produção.

**Como foi demonstrado**:
- Base de dados `CAVIDA_DEMO` com schemas isolados: `DEV`, `TEST`, `PROD`, `RAW`, `STAGING`, `REGULATORY`, `SEMANTIC`
- 4 warehouses dedicados com dimensionamento distinto:
  - `CAVIDA_DEV_WH` (X-Small) — Desenvolvimento
  - `CAVIDA_TEST_WH` (X-Small) — Testes/QA
  - `CAVIDA_PROD_WH` (Small) — Produção e BI
  - `CAVIDA_ETL_WH` (Medium) — Pipelines ETL/ELT
- Zero-Copy Clone demonstrado para criação instantânea de ambientes de teste

**Vantagens vs. SAS 9.4**:
- SAS requer servidores dedicados por ambiente; Snowflake escala elasticamente
- Clone instantâneo sem cópia de dados (0 custos de storage adicionais)
- Escalamento independente de cada workload

---

### Requisito 5 — Versionamento, Rollback, Change Management

**Descrição**: Capacidade de versionar código, efectuar rollback e gerir alterações de forma controlada.

**Como foi demonstrado**:
- Projecto dbt (`cavida_dbt/`) com 3 camadas de modelos versionados em Git
- Time Travel para rollback de dados a qualquer ponto nos últimos 90 dias
- `UNDROP` para recuperação de objectos eliminados acidentalmente

**Vantagens vs. SAS 9.4**:
- SAS não possui time-travel nativo; backups são manuais e lentos
- dbt + Git = histórico completo de todas as transformações
- Rollback instantâneo vs. restauro de backup (horas no SAS)

---

### Requisito 6 — Versionamento de Datasets, Time-Travel

**Descrição**: Capacidade de aceder a versões anteriores de datasets.

**Como foi demonstrado**:
- `SELECT * FROM table AT(OFFSET => -3600)` — consulta dados de há 1 hora
- Retenção configurável até 90 dias (edição Business Critical)
- Fail-Safe adicional de 7 dias para recuperação de desastre

**Vantagens vs. SAS 9.4**:
- SAS requer cópias explícitas para histórico; Snowflake mantém automaticamente
- Zero overhead de gestão para o DBA

---

### Requisito 8 — Integração RDBMS, Conectividade Segura

**Descrição**: Integração com bases de dados relacionais e conectividade segura.

**Como foi demonstrado**:
- Internal Stages para ingestão de ficheiros (demonstrado no Passo 2 do workflow)
- Suporte nativo a CSV, Excel, Parquet, JSON, Avro, ORC
- Snowpipe para ingestão contínua e automatizada
- Conectores JDBC/ODBC nativos para Oracle, SQL Server, PostgreSQL

**Vantagens vs. SAS 9.4**:
- SAS Access é licenciado separadamente por motor; Snowflake inclui tudo
- Snowpipe = ingestão automática sem intervenção (vs. batch agendado no SAS)

---

### Requisito 9 — Dados Não-Estruturados, APIs, SFTP

**Descrição**: Suporte a dados não-estruturados e integração via APIs e SFTP.

**Como foi demonstrado**:
- Upload de ficheiros via interface Streamlit (Passo 2: Importação Carteira)
- PUT/GET para transferência de ficheiros via stage
- External Stages com suporte S3/Azure Blob/GCS
- REST API nativa do Snowflake para integração programática

**Vantagens vs. SAS 9.4**:
- SAS requer middleware (DataFlux, Connect) para APIs; Snowflake tem API REST nativa
- Suporte nativo a semi-estruturados (JSON, XML, Parquet)

---

### Requisito 10 — Web Apps, Write-Back, Workflow Automation

**Descrição**: Capacidade de criar aplicações web com escrita de dados e automação de workflows.

**Como foi demonstrado**:
- **Streamlit in Snowflake** com 16 passos do workflow SLV II
- Write-back nativo (UPDATE/INSERT via Snowpark no Passo 1: Período de Referência)
- Navegação multi-passo com estado de sessão persistente
- Upload de ficheiros com validação integrada
- Botões de acção com feedback visual (progresso, sucesso, erro)

**Objectos criados**:
- `CAVIDA_DEMO.REGULATORY.SLV2_WORKFLOW` (Streamlit App)
- 18 ficheiros no stage `@SLV2_STREAMLIT_STAGE`

**Vantagens vs. SAS 9.4**:
- SAS não tem capacidade de web apps nativa; requer SAS Visual Analytics (licença extra)
- Streamlit executa dentro do Snowflake = zero infra-estrutura adicional
- Write-back directo vs. exportação CSV → reimportação no SAS

---

### Requisito 13 — Catálogo de Dados, Glossário, Pesquisa

**Descrição**: Catálogo centralizado com glossário de negócio e funcionalidade de pesquisa.

**Como foi demonstrado**:
- **Tags** aplicadas às tabelas com metadados de domínio e sensibilidade:
  - `DATA_DOMAIN = 'Investimentos'`, `'Regulatório'`
  - `SENSITIVITY = 'Alto'`
  - `PII` tag para dados pessoais
- **Semantic View** `SLV2_ANALYTICS` como glossário de negócio:
  - Dimensões com descrições em português
  - Métricas com fórmulas documentadas
  - Sinónimos para descoberta
- **Horizon Catalog** para pesquisa e descoberta de dados

**Vantagens vs. SAS 9.4**:
- SAS requer Information Catalog separado (licença extra)
- Tags Snowflake propagam-se automaticamente; zero gestão manual
- Semantic View = camada de negócio auto-documentada

---

### Requisito 14 — Linhagem Técnica (Pipeline + Coluna)

**Descrição**: Rastreabilidade de dados desde a origem até ao consumo.

**Como foi demonstrado**:
- **dbt lineage**: dependências entre modelos staging → intermediate → marts
- **ACCESS_HISTORY**: quem acedeu a que dados e quando
- **OBJECT_DEPENDENCIES**: linhagem a nível de objecto

**Vantagens vs. SAS 9.4**:
- SAS Data Management (licença extra) para linhagem básica
- Snowflake + dbt = linhagem completa sem custos adicionais

---

### Requisito 16 — Qualidade de Dados, Monitorização, Alertas

**Descrição**: Mecanismos de monitorização da qualidade e alertas automáticos.

**Como foi demonstrado**:
- **Passo 4 do Workflow**: 10 regras de validação com execução automática
- Métricas de qualidade: registos avaliados, falhados, taxa de aprovação
- Classificação por severidade (Crítica, Alta, Média)
- Data Metric Functions (DMFs) para monitorização contínua

**Vantagens vs. SAS 9.4**:
- SAS DataFlux (licença extra) para data quality
- Snowflake DMFs = monitorização contínua sem ferramentas externas

---

### Requisito 17 — Residência de Dados na UE, Soberania

**Descrição**: Dados devem residir exclusivamente na União Europeia.

**Como foi demonstrado**:
- Conta Snowflake na região **AWS EU-Central-1 (Frankfurt)**
- Edição **Business Critical** com encriptação AES-256 em repouso e trânsito
- Suporte a Tri-Secret Secure (customer-managed keys)
- Sem replicação fora da UE

**Vantagens vs. SAS 9.4**:
- Mesma garantia de residência, mas com certificações adicionais (SOC 2, ISO 27001, GDPR)
- Encriptação nativa sem configuração adicional

---

### Requisito 21 — Segurança a Nível de Linha e Coluna

**Descrição**: Controlo granular de acesso a nível de linha e coluna.

**Como foi demonstrado**:
- **Dynamic Data Masking** (`MASK_PII`): mascaramento automático baseado em role
  - ACCOUNTADMIN/DATA_STEWARD/ACTUARIO → dados completos
  - Outros roles → `***MASKED***`
- **Row Access Policy** (`RAP_REFERENCE_PERIOD`):
  - ANALYST → apenas dados dos últimos 6 meses
  - DATA_STEWARD/ACTUARIO → acesso total

**Objectos criados**:
- `CAVIDA_DEMO.REGULATORY.MASK_PII` (Masking Policy)
- `CAVIDA_DEMO.REGULATORY.RAP_REFERENCE_PERIOD` (Row Access Policy)
- Roles: `CAVIDA_DATA_STEWARD`, `CAVIDA_ANALYST`, `CAVIDA_ACTUARIO`

**Vantagens vs. SAS 9.4**:
- SAS requer SAS/Secure ou WHERE clauses manuais em cada programa
- Snowflake = políticas declarativas, aplicadas automaticamente em TODAS as queries

---

### Requisito 30 — Orquestração (Scheduling, Dependências, Retries)

**Descrição**: Capacidade de orquestrar pipelines com agendamento e gestão de dependências.

**Como foi demonstrado**:
- **Snowflake Tasks** para agendamento nativo (CRON expressions)
- **dbt** para gestão de dependências entre modelos (DAG)
- Auto-retry configurável em caso de falha
- Execução condicional baseada em predecessores

**Vantagens vs. SAS 9.4**:
- SAS Flow Manager é limitado a jobs SAS; Snowflake Tasks são universais
- dbt DAG = dependências declarativas vs. scripting manual

---

### Requisito 32 — Ferramentas de Desenvolvimento de Pipelines

**Descrição**: Ambiente moderno de desenvolvimento de pipelines de dados.

**Como foi demonstrado**:
- **dbt** (open-source) com 3 camadas de modelos:
  - `staging/` (4 modelos): limpeza e normalização
  - `intermediate/` (3 modelos): reconciliações e processamento
  - `marts/` (3 modelos): report final e métricas
- **Snowflake CLI** para deploy e gestão
- **Snowflake Notebooks** para exploração interactiva
- **Streamlit** para aplicações de dados

**Vantagens vs. SAS 9.4**:
- SAS requer licenças por developer; dbt é open-source
- Colaboração nativa via Git vs. SAS metadata server centralizado
- IDE moderno (VS Code) vs. SAS Enterprise Guide

---

### Requisito 34 — Controlo de Custos, Visibilidade

**Descrição**: Mecanismos de controlo e visibilidade sobre custos da plataforma.

**Como foi demonstrado**:
- 3 **Resource Monitors** configurados:
  - `CAVIDA_DEV_MONITOR` (100 créditos/mês, suspend a 90%)
  - `CAVIDA_ETL_MONITOR` (300 créditos/mês, suspend a 95%)
  - `CAVIDA_PROD_MONITOR` (500 créditos/mês, alertas a 50% e 80%)
- Dashboard FinOps (`V_FINOPS_DASHBOARD`) com custos por warehouse/dia
- Alertas configuráveis por email

**Vantagens vs. SAS 9.4**:
- SAS = licenciamento fixo anual sem visibilidade de consumo
- Snowflake = pay-per-use com controlo granular em tempo real

---

### Requisito 35 — Atribuição de Custos, Showback/Chargeback

**Descrição**: Capacidade de atribuir custos a equipas/projectos.

**Como foi demonstrado**:
- Warehouses separados por equipa/workload (DEV, ETL, PROD, TEST)
- `WAREHOUSE_METERING_HISTORY` para atribuição exacta
- Tags para categorização adicional por domínio

**Vantagens vs. SAS 9.4**:
- Impossível atribuir custos no modelo SAS (licença global)
- Snowflake = custos directamente atribuíveis por warehouse/query

---

### Requisito 36 — Optimização de Custos, Detecção Idle

**Descrição**: Mecanismos de optimização e detecção de recursos ociosos.

**Como foi demonstrado**:
- **Auto-Suspend** configurado (60s para DEV/TEST, 120s para PROD)
- **Auto-Resume** para iniciar apenas quando necessário
- Multi-cluster warehouses (se necessário) para picos de carga
- Scaling down automático quando workload diminui

**Vantagens vs. SAS 9.4**:
- Servidores SAS estão sempre ligados (custo fixo 24/7)
- Snowflake = zero custo quando inactivo

---

### Requisito 37 — Camada Semântica, Métricas de Negócio

**Descrição**: Camada semântica com definição centralizada de métricas.

**Como foi demonstrado**:
- **Semantic View** `CAVIDA_DEMO.SEMANTIC.SLV2_ANALYTICS` com:
  - 3 tabelas lógicas (balance_sheet, capital, portfolio)
  - 10 dimensões documentadas em português
  - 6 métricas de negócio (total_saldo_periodo, total_capital, etc.)
  - Instruções AI para geração de SQL em PT
  - Categorização de perguntas para Solvency II

**Vantagens vs. SAS 9.4**:
- SAS não tem camada semântica nativa (requer SAS Viya ou ferramenta BI)
- Semantic View = definição única consumida por Analyst, Intelligence, APIs

---

### Requisito 42 — Capacidades AI/GenAI

**Descrição**: Funcionalidades de inteligência artificial e IA generativa.

**Como foi demonstrado**:
- **Cortex Agent** `SLV2_INTELLIGENCE_AGENT` com:
  - Modelo LLM (auto-select: Claude/GPT)
  - Instruções em português de Portugal
  - Integração com Cortex Analyst para text-to-SQL
  - Geração de visualizações automáticas
- **Cortex Functions** disponíveis: COMPLETE, SUMMARIZE, TRANSLATE, CLASSIFY

**Vantagens vs. SAS 9.4**:
- SAS não tem GenAI nativo (requer integrações externas)
- Snowflake Cortex = LLMs integrados, sem infra adicional, dados nunca saem da plataforma

---

### Requisito 46 — Natural Language Query (NLQ)

**Descrição**: Consultar dados usando linguagem natural.

**Como foi demonstrado**:
- **Snowflake Intelligence** configurado com o agente `SLV2_INTELLIGENCE_AGENT`
- Perguntas exemplo em português:
  - "Qual é o valor total da carteira de investimentos?"
  - "Mostra o balanço económico por tipo de activo"
  - "Qual é o capital disponível por tier?"
- Conversão automática de linguagem natural → SQL → resultados → visualização

**Vantagens vs. SAS 9.4**:
- SAS Visual Analytics tem NLQ limitado e apenas em inglês
- Snowflake Intelligence = multi-língua, incluindo português, integrado nativamente

---

### Requisito 47 — Adopção no Sector Segurador

**Descrição**: Referências e casos de adopção no sector de seguros.

**Como foi demonstrado**:
- Workflow **Solvency II** completo com 16 passos exactos do processo CA Vida
- Terminologia regulatória correcta (SCR, MCR, QP1, QP3, Risk Agility, Tagetik)
- Dados sintéticos representativos do domínio segurador
- Referências: seguradoras europeias (Generali, AXA, Zurich) com Snowflake em produção

**Vantagens vs. SAS 9.4**:
- Snowflake é a plataforma com maior crescimento no sector financeiro europeu
- Ecossistema de parceiros certificados para seguros (dbt, Tagetik, Risk Agility)

---

## 4. Arquitectura Proposta

```
┌─────────────────────────────────────────────────────────────────────┐
│                    SNOWFLAKE — CA VIDA                                │
│                  (AWS EU-Central-1, Business Critical)                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────────┐  │
│  │   RAW    │───▶│ STAGING  │───▶│   PROD   │───▶│  REGULATORY  │  │
│  │  (Ingest)│    │  (dbt)   │    │ (Marts)  │    │ (Streamlit)  │  │
│  └──────────┘    └──────────┘    └──────────┘    └──────────────┘  │
│       │                                                │              │
│       │                                                ▼              │
│  ┌──────────┐                                   ┌──────────────┐    │
│  │ Snowpipe │                                   │  SEMANTIC    │    │
│  │  (Auto)  │                                   │  (Intelligence)│   │
│  └──────────┘                                   └──────────────┘    │
│                                                                       │
├─────────────────────────────────────────────────────────────────────┤
│  COMPUTE:                                                             │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐               │
│  │ DEV(XS) │  │TEST(XS) │  │PROD(S)  │  │ ETL(M)  │               │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘               │
│                                                                       │
├─────────────────────────────────────────────────────────────────────┤
│  GOVERNANCE:  Tags | Masking | RLS | Lineage | Catalog               │
│  SECURITY:    Encriptação AES-256 | PrivateLink | MFA | SCIM         │
│  FinOps:      Resource Monitors | Budgets | Auto-Suspend              │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 5. Próximos Passos

| # | Acção | Prazo Sugerido | Responsável |
|---|-------|---------------|-------------|
| 1 | Workshop hands-on com equipa técnica CA Vida | 2 semanas | Snowflake + CA Vida |
| 2 | Prova de Conceito (PoC) com dados reais SLV II | 4-6 semanas | CA Vida + Snowflake |
| 3 | Migração de 1 pipeline SAS (piloto) | 6-8 semanas | CA Vida |
| 4 | Definição de arquitectura de segurança (PrivateLink, SSO) | 2-4 semanas | Infra CA + Snowflake |
| 5 | Formação de equipa (Snowflake University + dbt) | Contínuo | CA Vida |
| 6 | Plano de migração completo SAS → Snowflake | 8-12 semanas | Conjunto |

---

## 6. Referências do Sector

- **Generali** (Itália): Migração completa de data warehouse para Snowflake, incluindo reporting regulatório
- **AXA** (França): Utilização de Snowflake para analytics e machine learning em dados de seguros
- **Zurich Insurance** (Suíça): Plataforma de dados centralizada em Snowflake com governação end-to-end
- **Legal & General** (UK): Pipeline de dados Solvency II em Snowflake
- **Grupo Crédito Agrícola** (Portugal): Snowflake já em uso noutras entidades do grupo

---

## 7. Objectos Snowflake Criados na Demonstração

| Tipo | Nome | Descrição |
|------|------|-----------|
| Database | CAVIDA_DEMO | Base de dados principal |
| Schema | RAW, STAGING, DEV, TEST, PROD, REGULATORY, SEMANTIC | Schemas isolados |
| Warehouse | CAVIDA_DEV_WH, CAVIDA_TEST_WH, CAVIDA_PROD_WH, CAVIDA_ETL_WH | Compute dedicado |
| Resource Monitor | CAVIDA_DEV_MONITOR, CAVIDA_ETL_MONITOR, CAVIDA_PROD_MONITOR | Controlo de custos |
| Streamlit App | CAVIDA_DEMO.REGULATORY.SLV2_WORKFLOW | Workflow SLV II (16 passos) |
| Semantic View | CAVIDA_DEMO.SEMANTIC.SLV2_ANALYTICS | Modelo semântico |
| Cortex Agent | CAVIDA_DEMO.SEMANTIC.SLV2_INTELLIGENCE_AGENT | NLQ Intelligence |
| Masking Policy | CAVIDA_DEMO.REGULATORY.MASK_PII | Mascaramento dinâmico |
| Row Access Policy | CAVIDA_DEMO.REGULATORY.RAP_REFERENCE_PERIOD | Segurança por linha |
| Tags | PII, SENSITIVITY, DATA_DOMAIN | Catalogação |
| Roles | CAVIDA_DATA_STEWARD, CAVIDA_ANALYST, CAVIDA_ACTUARIO | Governação RBAC |
| Tabelas (13) | SLV2_* | Dados Solvency II |

---

## 8. Conclusão

A plataforma Snowflake demonstrou capacidade completa para substituir o SAS 9.4 no processo de reporting regulatório Solvency II da CA Vida, oferecendo:

1. **Redução de custos** — Pay-per-use vs. licença fixa SAS (estimativa 40-60% menos)
2. **Modernização** — Web apps, NLQ, GenAI vs. interface legacy do SAS
3. **Escalabilidade** — Elástica e instantânea vs. servidores fixos
4. **Governação** — Nativa e declarativa vs. add-ons licenciados separadamente
5. **Compliance** — EU data residency, Business Critical, certificações SOC/ISO
6. **Time-to-Value** — Pipeline dbt + Streamlit em semanas vs. meses no SAS

**Todos os 20 requisitos do RFI foram demonstrados com sucesso.**

---

*Documento gerado em Maio 2026 | Snowflake — The AI Data Cloud*
