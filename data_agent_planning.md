# Customer Analytics Query Agent — Build Plan

> Created: 2026-06-26
> Updated: 2026-06-27
> Status: Phase 1 complete | Ready for Phase 2

## Project Goal

Build a POC (proof of concept) AI agent that answers natural-language business
questions about life insurance customer analytics. The agent converts questions
into SQL, executes against a DuckDB analytics database (loaded from a single
aggregated dataset), and returns results with plain-English summaries.

**Target user**: Business stakeholders in life insurance — marketing, distribution,
product, and executive teams who need fast answers to customer-related questions
without waiting for an analyst.

## Strategic Context

| Growth Motion | What It Means | Example Questions the Agent Answers |
|---|---|---|
| **Acquire** | New business analytics: channel effectiveness, conversion funnel, lead quality | "Show me new business premium by product and channel for Q2" |
| **Grow** | Cross-sell, up-sell: which customers should buy more | "What's the cross-sell rate for term customers with 3+ years tenure?" |
| **Retain** | Lapse/persistency: who is at risk and why | "Which segment has the highest 13-month lapse rate?" |
| **Optimize** | Distribution performance, campaign ROI, segment profitability | "Top 50 agents by NB premium with lapse rate and product mix" |

## Architecture

```
User (Streamlit UI)  →  Query Engine (NL → SQL)  →  SQL Executor  →  DuckDB
                              ↑                         ↓               ↑
                         Ollama LLM              Response Formatter     │
                         (llama3.1:8b)                 ↓               │
                              ↑                  Results (table+brief)  │
                         Knowledge Base                               Load
                    (schema, glossary, examples)                        │
                                                              wealth_segment_pivot
                                                                     .xlsx
```

**Components**:

| Component | Location | Responsibility |
|---|---|---|
| Knowledge Base | `src/agent/knowledge_base.py` | Table schema, column glossary, KPI formulas, few-shot Q&A examples |
| Query Engine | `src/agent/query_engine.py` | Sends prompt (schema + examples + question) to Ollama, parses SQL from response |
| SQL Executor | `src/agent/sql_executor.py` | Validates SQL (column existence, read-only), executes against DuckDB |
| Response Formatter | `src/agent/response_formatter.py` | Formats results as data tables + plain-English summary |
| Database Layer | `src/db/connection.py` | DuckDB connection, loads wealth_segment_pivot.xlsx |
| Web UI | `src/ui/app.py` | Streamlit app — question input, result display, SQL transparency |
| Config | `environment/config.py` | Ollama URL, model name, DuckDB path |

## Data Model

**Single source**: `data/generated/wealth_segment_pivot.xlsx`
- Requirements: [`dummy_data_gen_requirement.md`](dummy_data_gen_requirement.md)
- 57,600 rows, 12 columns, loaded into DuckDB as table `wealth_segment_pivot`

| # | Column | Type | Values |
|---|---|---|---|
| 1 | `life_stage` | Text | young single, young couple, matured adult, matured family with kid, matured family without kid, golden age |
| 2 | `wealth_segment` | Text | High-net-worth, Affluent, Mass |
| 3 | `customer_tenure` | Text | >= 1 year, 1-3 years, 3-6 years, 6-10 years, >10 years |
| 4 | `new_or_existing` | Text | New, Existing |
| 5 | `market` | Text | PHKL, PACS, PAMB, PBTB, PLAI, PSLA, PLUK, PVA, PLT, PCALT |
| 6 | `saving_holding` | Text | Yes, No |
| 7 | `investment_holding` | Text | Yes, No |
| 8 | `medical_holding` | Text | Yes, No |
| 9 | `critical_illness_holding` | Text | Yes, No |
| 10 | `others_health_and_protection_holding` | Text | Yes, No |
| 11 | `customer_count` | Integer | > 0 |
| 12 | `annual_premium` | Float | > 0 |

**This is an aggregated, pivot-ready dataset** — every row is a unique
combination of all 10 dimensions. Queries use GROUP BY, SUM, WHERE, and
proportion calculations against this single table.

## Build Phases

### Phase 1 — Dummy Data ✅

| Step | File | What It Does | Status |
|---|---|---|---|
| 1 | `dummy_data_gen_requirement.md` | Requirements spec for wealth_segment_pivot | ✅ |
| 2 | `scripts/01_generate_data.py` | Generate wealth_segment_pivot.xlsx (57,600 rows, seed 42) | ✅ |

### Phase 2 — Database Load & Knowledge Base

| Step | File | What It Does |
|---|---|---|
| 3 | `scripts/02_load_duckdb.py` | Load wealth_segment_pivot.xlsx into DuckDB table `wealth_segment_pivot` |
| 4 | `src/db/connection.py` | DuckDB connection manager (connect, load on startup) |
| 5 | `src/agent/knowledge_base.py` | Column glossary, KPI formulas, 15-20 few-shot Q&A examples |

### Phase 3 — Query Engine

| Step | File | What It Does |
|---|---|---|
| 6 | `src/agent/query_engine.py` | Prompt template: system prompt + column glossary + examples + user question → SQL |
| 7 | `src/agent/sql_executor.py` | SQL validation (column existence, read-only), execution |
| 8 | `src/agent/response_formatter.py` | Run query, return pandas DataFrame + plain-English summary |

### Phase 4 — Streamlit UI

| Step | File | What It Does |
|---|---|---|
| 9 | `src/ui/app.py` | Question input, submit button, loading state, results table + SQL panel |
| 10 | SQL transparency panel | Show generated SQL alongside results |
| 11 | Question history | Log recent questions and answers in session |

### Phase 5 — Testing & Refinement

| Step | File | What It Does |
|---|---|---|
| 12 | `tests/test_query_engine.py` | NL → SQL accuracy on known questions |
| 13 | `tests/test_sql_executor.py` | Validation and execution unit tests |
| 14 | `tests/test_knowledge_base.py` | Schema definitions match loaded DuckDB table |
| 15 | Manual QA | 15-20 real business questions, refine prompts and knowledge base |

### Phase 6 — Skills & Lessons Learned

| Step | What It Does |
|---|---|
| 16 | Populate `skills/nl-to-sql/SKILL.md` | NL-to-SQL prompt engineering for single-table queries |
| 17 | Populate `skills/data-generation/SKILL.md` | Aggregated data generation patterns |
| 18 | Log lessons learned during build | Continuous update to `lessons_learned/` |

## Agent Design Principles

1. **Safety first**: Agent never executes raw LLM output as SQL. All queries go through validation (column existence check, read-only).
2. **Read-only**: Agent has SELECT-only access to DuckDB.
3. **Explainability**: Every response includes the generated SQL — analyst can always verify.
4. **Graceful degradation**: If uncertain, the agent admits it and suggests rephrasing rather than returning wrong numbers.
5. **Knowledge-driven**: The knowledge base is the source of truth. The LLM augments but never overrides it.
6. **Pre-flight scan**: Before every job, scan `skills/` and `lessons_learned/` (AGENTS.md Rule 3).
7. **Documentation consistency**: When any doc changes, cross-check all related docs (AGENTS.md Rule 4).

## Success Criteria (POC)

- [ ] 60%+ of common customer analytics questions answered correctly on first try
- [ ] Response time under 30 seconds end-to-end
- [ ] Zero data errors (wrong column, wrong aggregation)
- [ ] Generated SQL is valid and explainable
- [ ] Streamlit UI is intuitive for non-technical stakeholders

## Development Workflow

```
python scripts/01_generate_data.py     # Generate wealth_segment_pivot.xlsx
python scripts/02_load_duckdb.py       # Load into DuckDB
streamlit run src/ui/app.py            # Launch the agent UI
```

## Current Status

| Phase | Status |
|---|---|
| Environment Setup | ✅ Complete |
| Phase 1 — Dummy Data | ✅ wealth_segment_pivot.xlsx (57,600 rows) |
| Phase 2 — DB Load & Knowledge Base | 🔴 Not started |
| Phase 3 — Query Engine | 🔴 Not started |
| Phase 4 — Streamlit UI | 🔴 Not started |
| Phase 5 — Testing | 🔴 Not started |
| Phase 6 — Skills & Lessons | 🔴 Not started |
