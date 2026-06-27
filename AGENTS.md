# AGENTS.md — AI Analytics Transformation

## Repository Rules (Hard Constraints)

1. **Workspace scope**: All modifications must happen exclusively within the
   repository root `C:\Users\Jason Huo\OneDrive\Documents\AI_Analytics_Transformation`.
   Modification of any file or directory outside this path is not allowed under
   any circumstance.

2. **Approval required**: Any modification to files in this repository (create,
   edit, delete, rename, or move) requires explicit approval from the repository
   owner before execution. No autonomous writes — propose first, execute only
   after confirmation.

3. **Pre-flight scan**: Before starting any job, the agent must scan the


4. **Documentation consistency**: When any specification, plan, or requirements
   document is created or updated, the agent must check and update all related
   documents to maintain cross-reference consistency. For example, if a new
   requirements doc (`dummy_data_gen_requirement.md`) is added, the build plan
   (`data_agent_planning.md`) must reference it and reflect its status. No
   document should become stale while its related documents evolve.
   `skills/` and `lessons_learned/` folders to load relevant capabilities and
   past learnings. This ensures every task builds on accumulated knowledge and
   avoids repeating known mistakes.

---

## Project Purpose

A POC (proof of concept) for an AI-agent-led Customer Analytics Query Agent
for life insurance. The agent converts natural-language business questions
into SQL, executes against a DuckDB analytics database, and returns results
with plain-English summaries.

## Technology Stack (POC phase)

- Python 3.12+ — primary development language
- DuckDB — embedded OLAP database (zero config, analytics-optimized)
- Streamlit — web UI for the agent interface
- Ollama — local LLM runtime (Llama 3.1 8B)
- Git — version control
- VS Code — IDE

## Directory Structure

```
AI_Analytics_Transformation/
├── AGENTS.md              # This file
├── README.md              # Project overview and setup guide
├── data/
│   ├── raw/               # Source CSVs (if any external data)
│   └── generated/         # Script-generated dummy data
├── scripts/
│   ├── 01_generate_data.py       # Dummy data generation
│   ├── 02_load_duckdb.py         # Load data into DuckDB
│   └── 03_validate_data.py       # Data quality checks
├── src/
│   ├── agent/
│   │   ├── __init__.py
│   │   ├── query_engine.py       # NL-to-SQL conversion (LLM integration)
│   │   ├── knowledge_base.py     # Table schemas, business glossary, few-shot examples
│   │   ├── sql_executor.py       # Safe SQL execution against DuckDB
│   │   └── response_formatter.py # Results formatting (tables, summaries)
│   ├── db/
│   │   ├── __init__.py
│   │   ├── connection.py         # DuckDB connection manager
│   │   └── schema.py             # DDL for tables and views
│   └── ui/
│       ├── __init__.py
│       └── app.py                # Streamlit app
├── tests/
│   ├── test_query_engine.py
│   ├── test_sql_executor.py
│   └── test_knowledge_base.py
├── skills/
│   └── README.md                 # Skill registry (what each skill does, when to use)
├── lessons_learned/
│   └── README.md                 # Index of all lessons (date, context, resolution)
├── docs/
│   ├── data_dictionary.md        # All tables, columns, business definitions
│   └── question_patterns.md      # Catalog of supported question types
└── .gitignore
```

### `skills/` Folder

Purpose: store reusable capabilities, prompts, templates, and tool configurations
that agents load contextually. Each skill lives in its own subfolder.

**Skill format** — each skill is a subfolder containing a `SKILL.md` file:
```
skills/
├── README.md                     # Registry of all skills
├── nl-to-sql/                    # Skill: natural language → SQL generation
│   └── SKILL.md                  # Instructions for the skill
├── data-generation/              # Skill: dummy data generation patterns
│   └── SKILL.md
├── duckdb-query-patterns/        # Skill: common DuckDB query templates
│   └── SKILL.md
└── streamlit-patterns/           # Skill: Streamlit UI conventions
    └── SKILL.md
```

Each `SKILL.md` must include:
- **Name**: short, descriptive
- **When to use**: conditions that trigger this skill
- **Instructions**: step-by-step guidance for the agent
- **Examples**: concrete usage examples

### `lessons_learned/` Folder

Purpose: a living log of every mistake, error, blocker, and resolution
encountered during the project. Updated immediately after each incident.

**Entry format** — each lesson is a Markdown file named by date and topic:
```
lessons_learned/
├── README.md                              # Chronological index
├── 2026-06-26_ollama-model-timeout.md     # Example entry
├── 2026-06-27_sql-generation-hallucination.md
└── 2026-07-01_duckdb-date-casting-error.md
```

Each entry must include:
- **Date**: when it happened
- **Context**: what we were trying to do
- **Error**: exact error message or behavior observed
- **Root cause**: why it happened
- **Resolution**: what fixed it
- **Prevention**: how to avoid it going forward (this becomes input for skills or rules)

## Coding Conventions

### Python
- Python 3.12+, use type hints on all function signatures
- Follow PEP 8 with 100-char line limit
- Use `pathlib.Path` for all file paths (never string concatenation)
- Use `logging` module (never `print` for application output)
- Docstrings: Google style for public functions, concise one-liners for private helpers
- Dependencies managed via `requirements.txt` (not Poetry/pipenv for POC simplicity)

### SQL
- All table and column names: `snake_case`
- DuckDB dialect — prefer its analytics functions over vanilla SQL
- Views for common query patterns live in `src/db/schema.py`
- Never concatenate user input into SQL strings; use parameterized queries

### Git
- Branch naming: feature branches off `main`
- Commit messages: imperative mood, present tense, under 72 chars
- No committed data files > 10 MB
- No committed secrets, API keys, or connection strings

### Data Handling
- All dummy data must be clearly synthetic — no real customer data in the POC
- Data generation scripts must be deterministic (fixed random seed) for reproducibility
- Sensitive-like fields (names, IDs) must use Faker library, never real values
- DuckDB file (`*.duckdb`) is gitignored — generated locally on setup

## Agent Design Principles

1. **Safety first**: Agent never executes raw user input as SQL. All queries go
   through a validation layer that checks table/column existence before execution.
2. **Read-only**: Agent has SELECT-only access to DuckDB. No INSERT/UPDATE/DELETE.
3. **Explainability**: Every agent response includes the generated SQL so the
   analyst can verify correctness.
4. **Graceful degradation**: If the LLM is uncertain, the agent admits it and
   suggests rephrasing rather than guessing with wrong numbers.
5. **Knowledge-driven**: The knowledge base (schemas, glossary, few-shot examples)
   is the primary source of truth. The LLM augments it but never overrides it.

## Testing Standards

- Unit tests for every module in `src/agent/` and `src/db/`
- Integration tests: end-to-end from natural language → SQL → correct results
- Test data: a small, fixed DuckDB database checked into `tests/fixtures/`
- All tests must pass before merging to `main`
- Run tests with: `python -m pytest tests/ -v`

## Life Insurance Domain Conventions

- **NB Premium** (New Business Premium): first-year premium from new policies
- **Persistency**: % of policies still in-force at month N (13-month and 25-month are key metrics)
- **Lapse**: policy termination by non-payment (not death/maturity/surrender)
- **Cross-sell**: selling an additional product to an existing policyholder
- **Sum Assured**: the guaranteed death benefit amount
- **APE** (Annual Premium Equivalent): regular premium + 10% of single premium
- **Distribution channels**: Agency, Bancassurance, Broker, Digital/Direct
- **Customer segments**: Mass, Mass Affluent, HNW (High Net Worth)
- **Product types**: Term Life, Whole Life, Endowment, Universal Life, Critical Illness Rider

## Development Workflow

1. `python scripts/01_generate_data.py` — generate dummy data
2. `python scripts/02_load_duckdb.py` — load into DuckDB
3. `python scripts/03_validate_data.py` — run quality checks
4. `streamlit run src/ui/app.py` — launch the agent UI
5. Iterate: ask questions, review SQL, refine knowledge base

