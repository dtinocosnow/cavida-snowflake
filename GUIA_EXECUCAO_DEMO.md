# Guia de Execução da Demo — CA Vida Solvency II
## Duração Total: 1h30min | Plataforma Snowflake

---

## Preparação (5 min antes)

1. Abrir Snowsight: https://app.snowflake.com/sfseeurope/dtinoco_aws/
2. Ter abertos em tabs:
   - **Notebook**: `CAVIDA_DEMO.REGULATORY.CAVIDA_DEMO_V2_EXECUCAO` ← PRINCIPAL
   - **Streamlit App**: `CAVIDA_DEMO.REGULATORY.SLV2_WORKFLOW`
   - **Snowflake Intelligence**: Agent `CA Vida - Solvency II Intelligence`
   - **GitHub**: https://github.com/dtinocosnow/cavida-snowflake
3. Verificar warehouses: `SHOW WAREHOUSES LIKE 'CAVIDA%';`

---

## Storytelling: O Fio Condutor

> "Imaginem que já fizemos a migração do SAS 9.4. Estou a mostrar-vos o resultado — um projecto real, versionado em Git, com pipelines declarativos, governação nativa e uma aplicação web que substitui os vossos 16 passos manuais. Tudo dentro de Snowflake, sem ferramentas externas."

---

## Fluxo Completo

| ACT | Duração | Onde | Tema |
|-----|---------|------|------|
| 1 - Platform | 25 min | Notebook + Snowsight | Infra, Git, dbt, Time Travel, Clone |
| 2 - Governance | 20 min | Notebook | Tags, EU, Masking, RLS |
| 3 - Streamlit | 25 min | Streamlit App | 16 passos SLV II |
| 4 - FinOps | 10 min | Notebook | Monitors, custos, auto-suspend |
| 5 - Intelligence | 10 min | Snowflake Intelligence | NLQ em português |

---

## ACT 1: Platform Foundation (25 min)

### 1.1 — Git Integration & Version Control (5 min)

**💬 Storytelling**: "Todo o código deste projecto — pipelines, app, scripts — vive num repositório Git. O Snowflake sincroniza-se directamente com o GitHub. Cada alteração é rastreável, cada versão é recuperável. Isto é change management real."

**Acções**:
1. Abrir GitHub: https://github.com/dtinocosnow/cavida-snowflake
   - Mostrar estrutura: `cavida_dbt/`, `streamlit_slv2/`, `notebooks/`, scripts
   - Mostrar último commit com hash e timestamp
2. No Snowsight: navegar a CAVIDA_DEMO → REGULATORY → Git Repositories → `CAVIDA_REPO`
   - Mostrar que Snowflake tem clone completo do repo
   - Mostrar branch `main` sincronizada
3. No Notebook: executar query de verificação

**Pontos-chave**:
- Código versionado = auditoria completa (quem, quando, o quê)
- Branch strategy: `main` = produção, feature branches para dev
- Promotion controlada: PR → code review → merge → FETCH no Snowflake
- Rollback instantâneo: revert de commit = voltar a qualquer versão

**💬 Frase killer**: "No SAS, o código vive em metadata servers opacos. Aqui, está no Git — universal, auditável, colaborativo."

---

### 1.2 — Arquitectura Multi-Ambiente (5 min)

**💬 Storytelling**: "Cada equipa tem o seu próprio compute. Se o pipeline ETL escalar para processar mais dados, não afecta a produção nem os analistas. E escalar leva 2 segundos."

**No Notebook**: Executar células SHOW WAREHOUSES + SHOW SCHEMAS + ALTER WAREHOUSE

**Pontos-chave**:
- 4 warehouses isolados (DEV XS, TEST XS, PROD S, ETL M)
- Escalar/reduzir em 2 segundos
- Auto-suspend: custo ZERO quando inactivo

---

### 1.3 — Zero-Copy Clone (3 min)

**💬 Storytelling**: "Precisam de um ambiente de teste com os mesmos dados de produção? No SAS copiam terabytes durante horas. Aqui, é instantâneo e ocupa zero bytes adicionais."

**No Notebook**: Executar CREATE SCHEMA TEST CLONE PROD

**Pontos-chave**:
- < 1 segundo independentemente do volume
- 0 bytes extra até divergir
- Perfeito para QA, UAT, sandbox de desenvolvimento

---

### 1.4 — Time Travel (5 min)

**💬 Storytelling**: "Alguém apagou dados por engano numa sexta-feira à noite? No SAS, restauram backup no fim-de-semana. Aqui, recuperamos em 3 segundos — até 90 dias de histórico automático."

**No Notebook**: Executar sequência DELETE → AT(OFFSET) → INSERT restore

**Pontos-chave**:
- 90 dias automáticos (Business Critical)
- UNDROP para tabelas, schemas, bases de dados inteiras
- Zero configuração, zero gestão

---

### 1.5 — dbt Project: Pipeline como Código (7 min)

**💬 Storytelling**: "Este pipeline substitui centenas de programas SAS. Está deployado como objecto Snowflake nativo, com dependências declarativas e resultados auditáveis. E vive no mesmo Git que acabámos de ver."

**Acções**:
1. No Notebook: mostrar objectos criados (10 modelos)
2. No Snowsight: CAVIDA_DEMO → REGULATORY → dbt Projects → `CAVIDA_SLV2_PROJECT`
   - Mostrar DAG visual (staging → intermediate → marts)
   - Mostrar execution history: 10/10 PASS
3. Ligar ao Git: "Este dbt project é o mesmo código que viram no GitHub em `cavida_dbt/`"

**Pontos-chave**:
- Pipeline declarativo vs. procedural (SAS)
- Linhagem automática (DAG)
- Testes integrados
- Deployed nativamente no Snowflake (não requer servidor externo)

**💬 Frase killer**: "No Databricks não existe dbt deploy nativo. No BigQuery também não. Só no Snowflake o dbt vive como objecto gerido."

---

## ACT 2: Governance & Security (20 min)

### 2.1 — Catálogo, Tags & Camada Semântica (5 min)

**💬 Storytelling**: "Cada tabela está classificada por domínio e sensibilidade. E a Semantic View funciona como glossário de negócio — as vossas métricas definidas centralmente, em português."

**No Notebook**: Executar SHOW TAGS + SHOW SEMANTIC DIMENSIONS/METRICS

**Pontos-chave**:
- Tags: DATA_DOMAIN, SENSITIVITY, PII — propagam automaticamente
- Semantic View = definição única de métricas consumida por Intelligence, APIs, BI
- Zero licenças adicionais (no SAS = Information Catalog extra)

---

### 2.2 — EU Data Residency (2 min)

**💬 Storytelling**: "Os dados da CA Vida nunca saem da UE. Frankfurt, Business Critical, encriptação AES-256. Conformidade RGPD total."

**No Notebook**: Executar SELECT CURRENT_REGION()

---

### 2.3 — Dynamic Data Masking (5 min)

**💬 Storytelling**: "O actuário vê todos os dados. O analista vê dados mascarados. Não há código para manter — é uma política declarativa aplicada em TODAS as queries automaticamente."

**No Notebook**: Executar query como ACCOUNTADMIN → depois como CAVIDA_ANALYST

**Pontos-chave**:
- Masking baseado em role (zero código)
- Aplica-se em todas as queries, views, exports — impossível contornar
- No SAS: WHERE clauses manuais em cada programa

---

### 2.4 — Row-Level Security (5 min)

**💬 Storytelling**: "O analista só vê dados dos últimos 6 meses. Não recebe erro — simplesmente não vê os dados históricos. Segurança invisível."

**No Notebook**: Executar GROUP BY reference_date como ADMIN → depois como ANALYST

**Pontos-chave**:
- Filtro por data de referência (últimos 6 meses para analistas)
- Invisível para o utilizador
- Data minimisation (RGPD compliance)

---

### 2.5 — Lineage (3 min)

**💬 Storytelling**: "De onde vêm estes dados? Quem os transformou? O grafo do dbt dá-vos linhagem completa — da origem ao report final."

**No Snowsight**: Abrir dbt project → mostrar grafo visual
- `stg_investment_portfolio` → `int_asset_reconciliation` → `mart_economic_balance_sheet`

---

## ACT 3: Workflow Solvency II — Streamlit (25 min)

**💬 Storytelling de abertura**: "Tudo o que viram até agora é infra-estrutura. Agora vamos ver o resultado para o utilizador final — o vosso processo SLV II de 16 passos, replicado como aplicação web nativa no Snowflake. Sem servidores adicionais, sem licenças de SAS Visual Analytics."

### Abrir: Streamlit App `SLV2_WORKFLOW`

**Percorrer cada passo com narrativa**:

| Passo | Storytelling |
|-------|-------------|
| 1 - Período Referência | "O actuário actualiza o período directamente na app — write-back instantâneo sem exports." |
| 2 - Importação Carteira | "Upload do ficheiro Excel directamente na interface. Sem SFTP, sem processos batch." |
| 3 - Estado CA Gestl | "Visibilidade em tempo real do carregamento — status colorido, barra de progresso." |
| 4 - Regras Validação | "10 regras executam automaticamente. No SAS era verificação manual." |
| 5 - Reconciliação | "Totais por classe de activo com export para Excel integrado." |
| 6-8 - Risk Agility | "Reconciliação de activos e passivos, registos vazios por ficheiro." |
| 9-11 - Download/Import | "Gestão de ficheiros Risk Agility — download, import, estado." |
| 12 - Tagetik | "Carregamento com pré-requisitos validados automaticamente." |
| 13 - Capital | "Capital disponível por tier — métricas em M€." |
| 14 - Balanço | "Balanço económico com variações e delta indicator." |
| 15 - Fecho | "Um botão fecha o report. Sem batch jobs, sem esperar." |
| 16 - Download | "Ficheiros finais para Tagetik disponíveis imediatamente." |

**💬 Frase killer de fecho**: "16 passos, tudo dentro de Snowflake. Zero infra externa. No Databricks e BigQuery isto simplesmente não existe."

---

## ACT 4: FinOps & Cost Intelligence (10 min)

**💬 Storytelling**: "Quanto custa correr tudo isto? Ao contrário do SAS com licença fixa anual sem visibilidade — aqui sabemos exactamente quanto custa cada equipa, cada query. E quando ninguém usa, o custo é literalmente zero."

**No Notebook**: Executar células Resource Monitors + Cost by Warehouse

**Pontos-chave**:
- 3 Resource Monitors com alertas automáticos (50%, 80%, 95%)
- Custo por warehouse = atribuição exacta por equipa
- Auto-suspend (60s/120s): noite e fim-de-semana = 0€
- Estimativa: 40-60% menos que licença SAS equivalente

---

## ACT 5: WOW Factor — Snowflake Intelligence (10 min)

**💬 Storytelling**: "E agora, o futuro. Imaginem que qualquer pessoa da CA Vida — actuário, gestor, compliance — pode simplesmente PERGUNTAR aos dados em português. Sem saber SQL. Sem pedir relatórios. Vejam."

### Abrir: Snowflake Intelligence → Agent `CA Vida - Solvency II Intelligence`

**Demo ao vivo (4 perguntas)**:
1. "Qual é o valor total da carteira de investimentos?"
   - *Mostrar SQL gerado, resultado formatado*
2. "Mostra o balanço económico por tipo de activo"
   - *Mostrar tabela + visualização automática*
3. "Qual é o capital disponível por tier?"
   - *Mostrar breakdown Tier 1/2/3*
4. "Quantos instrumentos temos por classe de activo?"
   - *Mostrar gráfico gerado automaticamente*

**💬 Frase killer**: "Isto é EXCLUSIVO Snowflake. Não existe no SAS. Não existe no Databricks nativamente. Não existe no BigQuery. É a vossa equipa de business intelligence — disponível 24/7, em português."

---

## Encerramento (5 min)

### Resumo (mostrar última célula do Notebook)

**💬 Storytelling de fecho**: "Acabámos de ver, em 90 minutos, a substituição completa do SAS 9.4: pipelines, aplicação web, governação, segurança, controlo de custos, e inteligência artificial — tudo nativo, tudo numa única plataforma, tudo na UE."

- ✅ 20/20 requisitos RFI demonstrados
- ✅ Substituição completa do SAS 9.4
- ✅ Zero licenças adicionais para governance, quality, ou AI
- ✅ Código no Git, auditável, versionado
- ✅ EU data residency (Frankfurt, Business Critical)

### Call-to-Action

| # | Acção | Prazo |
|---|-------|-------|
| 1 | Workshop hands-on com equipa técnica | 2 semanas |
| 2 | PoC com dados reais SLV II | 4-6 semanas |
| 3 | Migração piloto de 1 pipeline SAS | 6-8 semanas |
| 4 | Plano de migração completo | 8-12 semanas |

### Entregável
- Relatório detalhado enviado após sessão: `RELATORIO_DEMONSTRACAO_CA_VIDA.md`
- Repositório Git com todo o código: https://github.com/dtinocosnow/cavida-snowflake

---

## Objectos Snowflake da Demo

| Tipo | Objecto | ACT |
|------|---------|-----|
| Git Repository | `CAVIDA_DEMO.REGULATORY.CAVIDA_REPO` | 1.1 |
| Notebook | `CAVIDA_DEMO.REGULATORY.CAVIDA_DEMO_V2_EXECUCAO` | 1-4 |
| dbt Project | `CAVIDA_DEMO.REGULATORY.CAVIDA_SLV2_PROJECT` | 1.5 |
| Streamlit | `CAVIDA_DEMO.REGULATORY.SLV2_WORKFLOW` | 3 |
| Semantic View | `CAVIDA_DEMO.SEMANTIC.SLV2_ANALYTICS` | 2.1, 5 |
| Cortex Agent | `CAVIDA_DEMO.SEMANTIC.SLV2_INTELLIGENCE_AGENT` | 5 |
| API Integration | `CAVIDA_GIT_INTEGRATION` | 1.1 |

---

## Perguntas Difíceis — Respostas Preparadas

| Pergunta | Resposta |
|----------|----------|
| "E se o warehouse ficar lento?" | "ALTER WAREHOUSE SET SIZE = LARGE — 2 segundos, sem reiniciar." |
| "Como fazem backup?" | "Time Travel 90d + Fail-Safe 7d + Replication cross-region." |
| "Quanto custa?" | "Pay-per-use. Estimativa no sizing. Sem licenças fixas." |
| "E a migração SAS?" | "dbt + SnowConvert. Pipeline piloto em 6-8 semanas." |
| "Quem mais usa no sector?" | "Generali, AXA, Zurich, Legal&General — todos em produção." |
| "E o Databricks?" | "Sem Streamlit, sem NLQ, sem dbt nativo, sem clone instantâneo, clusters caros." |
| "E o BigQuery?" | "Sem apps web, sem dbt deploy, 7d time travel, sem clone, sem Intelligence." |
| "A migração demora?" | "Pipeline piloto: 6-8 sem. Full: 6-12 meses conforme complexidade." |
| "E controlo de versões?" | "Git nativo — repo sincronizado no Snowflake. Mesmo que viram." |
| "Podemos testar?" | "Trial account grátis 30 dias. PoC em 4-6 semanas com dados reais." |

---

*Tempo total: 90 minutos | Executar notebook célula-a-célula + Streamlit + Intelligence*
