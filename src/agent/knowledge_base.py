"""Knowledge base for the Customer Analytics Query Agent.

This module defines the table schema, column glossary, synonym mappings,
KPI formulas, and few-shot examples that ground the LLM when generating SQL.
"""

# ═══════════════════════════════════════════════════════════════════════
# TABLE SCHEMA
# ═══════════════════════════════════════════════════════════════════════

TABLE_NAME = "wealth_segment_pivot"

SCHEMA_DDL = """
CREATE TABLE wealth_segment_pivot (
    life_stage VARCHAR,
    wealth_segment VARCHAR,
    customer_tenure VARCHAR,
    new_or_existing VARCHAR,
    market VARCHAR,
    saving_holding VARCHAR,
    investment_holding VARCHAR,
    medical_holding VARCHAR,
    critical_illness_holding VARCHAR,
    others_health_and_protection_holding VARCHAR,
    customer_count INTEGER,
    annual_premium DOUBLE
)
"""

# ═══════════════════════════════════════════════════════════════════════
# COLUMN GLOSSARY
# ═══════════════════════════════════════════════════════════════════════

COLUMN_GLOSSARY = [
    {
        "column": "life_stage",
        "type": "VARCHAR",
        "description": "Customer life stage category",
        "values": [
            "young single", "young couple", "matured adult",
            "matured family with kid", "matured family without kid",
            "golden age",
        ],
    },
    {
        "column": "wealth_segment",
        "type": "VARCHAR",
        "description": "Customer wealth tier — used for proportion calculations",
        "values": ["High-net-worth", "Affluent", "Mass"],
    },
    {
        "column": "customer_tenure",
        "type": "VARCHAR",
        "description": "How long the customer has been with the company",
        "values": [
            ">= 1 year", "1-3 years", "3-6 years", "6-10 years", ">10 years",
        ],
    },
    {
        "column": "new_or_existing",
        "type": "VARCHAR",
        "description": "Whether the customer is new or existing",
        "values": ["New", "Existing"],
    },
    {
        "column": "market",
        "type": "VARCHAR",
        "description": "Business market/entity code (also called LBU, local business unit)",
        "values": [
            "PHKL", "PACS", "PAMB", "PBTB", "PLAI",
            "PSLA", "PLUK", "PVA", "PLT", "PCALT",
        ],
    },
    {
        "column": "saving_holding",
        "type": "VARCHAR",
        "description": "Whether the customer holds a savings product",
        "values": ["Yes", "No"],
    },
    {
        "column": "investment_holding",
        "type": "VARCHAR",
        "description": "Whether the customer holds an investment product",
        "values": ["Yes", "No"],
    },
    {
        "column": "medical_holding",
        "type": "VARCHAR",
        "description": "Whether the customer holds a medical insurance product",
        "values": ["Yes", "No"],
    },
    {
        "column": "critical_illness_holding",
        "type": "VARCHAR",
        "description": "Whether the customer holds a critical illness product",
        "values": ["Yes", "No"],
    },
    {
        "column": "others_health_and_protection_holding",
        "type": "VARCHAR",
        "description": "Whether the customer holds other health/protection products",
        "values": ["Yes", "No"],
    },
    {
        "column": "customer_count",
        "type": "INTEGER",
        "description": "Number of customers in this combination. Always > 0. Use SUM() for totals.",
        "values": "Integer > 0",
    },
    {
        "column": "annual_premium",
        "type": "DOUBLE",
        "description": "Total annual premium for this combination. Use SUM() for totals, SUM(annual_premium)/SUM(customer_count) for average.",
        "values": "Float > 0",
    },
]

# ═══════════════════════════════════════════════════════════════════════
# SYNONYMS
# ═══════════════════════════════════════════════════════════════════════

COLUMN_SYNONYMS: dict[str, str] = {
    # ── market ──
    "LBU": "market",
    "lbu": "market",
    "local market": "market",
    "local business unit": "market",
    "business unit": "market",
    "entity": "market",
    "market code": "market",
    "country": "market",
    # ── wealth_segment ──
    "segment": "wealth_segment",
    "customer segment": "wealth_segment",
    "customer tier": "wealth_segment",
    "wealth tier": "wealth_segment",
    "wealth band": "wealth_segment",
    "customer band": "wealth_segment",
    # ── customer_tenure ──
    "tenure": "customer_tenure",
    "years with us": "customer_tenure",
    "relationship length": "customer_tenure",
    "customer age": "customer_tenure",
    "tenure band": "customer_tenure",
    # ── customer_count ──
    "number of customers": "customer_count",
    "customer base": "customer_count",
    "customer volume": "customer_count",
    "policy count": "customer_count",
    "count of customers": "customer_count",
    "customer numbers": "customer_count",
    "how many customers": "customer_count",
    # ── annual_premium ──
    "premium": "annual_premium",
    "APE": "annual_premium",
    "annual premium equivalent": "annual_premium",
    "revenue": "annual_premium",
    "premium income": "annual_premium",
    "premium volume": "annual_premium",
    "GWP": "annual_premium",
    "gross written premium": "annual_premium",
    # ── life_stage ──
    "life cycle": "life_stage",
    "demographic": "life_stage",
    "life stage group": "life_stage",
    # ── new_or_existing ──
    "customer type": "new_or_existing",
    "new vs existing": "new_or_existing",
    "acquisition type": "new_or_existing",
    "new customer": "new_or_existing",
    "existing customer": "new_or_existing",
    # ── holding columns ──
    "savings product": "saving_holding",
    "has savings": "saving_holding",
    "savings": "saving_holding",
    "investment product": "investment_holding",
    "has investments": "investment_holding",
    "investments": "investment_holding",
    "medical insurance": "medical_holding",
    "health insurance": "medical_holding",
    "medical": "medical_holding",
    "CI": "critical_illness_holding",
    "critical illness": "critical_illness_holding",
    "CI product": "critical_illness_holding",
    "other health": "others_health_and_protection_holding",
    "other protection": "others_health_and_protection_holding",
    "health and protection": "others_health_and_protection_holding",
}

VALUE_SYNONYMS: dict[str, str] = {
    # ── wealth_segment values ──
    "HNW": "High-net-worth",
    "HNWI": "High-net-worth",
    "high net worth": "High-net-worth",
    "high value": "High-net-worth",
    "premium segment": "High-net-worth",
    "mass affluent": "Affluent",
    "mid-tier": "Affluent",
    "middle": "Affluent",
    "mass market": "Mass",
    "standard": "Mass",
    "regular": "Mass",
    "low tier": "Mass",
    # ── new_or_existing values ──
    "new business": "New",
    "newly acquired": "New",
    "new customer": "New",
    "existing customer": "Existing",
    "in-force": "Existing",
    "renewal": "Existing",
    # ── tenure values ──
    "less than 1 year": ">= 1 year",
    "short tenure": ">= 1 year",
    "1 year": ">= 1 year",
    "1 to 3 years": "1-3 years",
    "3 to 6 years": "3-6 years",
    "6 to 10 years": "6-10 years",
    "over 10 years": ">10 years",
    "10 years plus": ">10 years",
    "long tenure": ">10 years",
}


def build_synonym_rules() -> str:
    """Build a compact synonym reference for the LLM prompt."""
    rules: list[str] = []
    rules.append("SYNONYM RULES — when the user mentions any of these, use the mapped term:\n")
    rules.append("Column synonyms (term → actual column name):")
    for syn, col in sorted(COLUMN_SYNONYMS.items()):
        rules.append(f'  "{syn}" → {col}')
    rules.append("\nValue synonyms (term → actual column value):")
    for syn, val in sorted(VALUE_SYNONYMS.items()):
        rules.append(f'  "{syn}" → {val}')
    return "\n".join(rules)


# ═══════════════════════════════════════════════════════════════════════
# KPI FORMULAS
# ═══════════════════════════════════════════════════════════════════════

KPI_FORMULAS = {
    "total_customers": "SUM(customer_count)",
    "total_premium": "SUM(annual_premium)",
    "avg_premium_per_customer": "SUM(annual_premium) / SUM(customer_count)",
    "wealth_segment_proportion": (
        "SUM(customer_count) FILTER (WHERE wealth_segment = '<segment>') / "
        "SUM(customer_count)"
    ),
    "product_holding_rate": (
        "SUM(customer_count) FILTER (WHERE <product>_holding = 'Yes') / "
        "SUM(customer_count)"
    ),
}

# ═══════════════════════════════════════════════════════════════════════
# FEW-SHOT EXAMPLES
# ═══════════════════════════════════════════════════════════════════════

FEW_SHOT_EXAMPLES: list[dict] = [
    # ── Pattern: Simple aggregation by one dimension ──
    {
        "question": "How many customers do we have in total?",
        "sql": "SELECT SUM(customer_count) AS total_customers FROM wealth_segment_pivot",
        "notes": "Simple total — no GROUP BY needed",
    },
    {
        "question": "What is the total annual premium across all markets?",
        "sql": "SELECT SUM(annual_premium) AS total_premium FROM wealth_segment_pivot",
        "notes": "Simple total of annual_premium",
    },
    {
        "question": "Show me customer count by wealth segment.",
        "sql": "SELECT wealth_segment, SUM(customer_count) AS total_customers, SUM(annual_premium) AS total_premium FROM wealth_segment_pivot GROUP BY wealth_segment",
        "notes": "Group by one dimension — always include both metrics for completeness",
    },
    # ── Pattern: Filter by market, group by one dimension ──
    {
        "question": "What is the customer breakdown by wealth segment in PHKL?",
        "sql": "SELECT wealth_segment, SUM(customer_count) AS total_customers, SUM(annual_premium) AS total_premium FROM wealth_segment_pivot WHERE market = 'PHKL' GROUP BY wealth_segment",
        "notes": "WHERE before GROUP BY — filter to one market, then aggregate",
    },
    {
        "question": "Show me the premium by life stage for PACS.",
        "sql": "SELECT life_stage, SUM(customer_count) AS total_customers, SUM(annual_premium) AS total_premium FROM wealth_segment_pivot WHERE market = 'PACS' GROUP BY life_stage",
        "notes": "Single-market filter with different grouping dimension",
    },
    # ── Pattern: Filter by segment, group by market (cross-market comparison) ──
    {
        "question": "How many HNW customers does each market have?",
        "sql": "SELECT market, SUM(customer_count) AS total_customers, SUM(annual_premium) AS total_premium FROM wealth_segment_pivot WHERE wealth_segment = 'High-net-worth' GROUP BY market",
        "notes": "Apply value synonym: HNW → High-net-worth. Filter to one segment, compare across markets.",
    },
    {
        "question": "Compare the Affluent segment customer count and premium across all LBUs.",
        "sql": "SELECT market, SUM(customer_count) AS total_customers, SUM(annual_premium) AS total_premium FROM wealth_segment_pivot WHERE wealth_segment = 'Affluent' GROUP BY market ORDER BY market",
        "notes": "Apply synonym: LBU → market. ORDER BY for clean comparison.",
    },
    # ── Pattern: Multi-dimension grouping ──
    {
        "question": "Show me customer count by wealth segment and life stage for PHKL.",
        "sql": "SELECT wealth_segment, life_stage, SUM(customer_count) AS total_customers, SUM(annual_premium) AS total_premium FROM wealth_segment_pivot WHERE market = 'PHKL' GROUP BY wealth_segment, life_stage ORDER BY wealth_segment, life_stage",
        "notes": "Two GROUP BY dimensions for a matrix view",
    },
    {
        "question": "Break down customer count by market and customer tenure.",
        "sql": "SELECT market, customer_tenure, SUM(customer_count) AS total_customers FROM wealth_segment_pivot GROUP BY market, customer_tenure ORDER BY market, customer_tenure",
        "notes": "Cross-market comparison with tenure breakout",
    },
    # ── Pattern: New vs Existing comparison ──
    {
        "question": "How do new customers compare to existing customers in terms of premium in PHKL?",
        "sql": "SELECT new_or_existing, SUM(customer_count) AS total_customers, SUM(annual_premium) AS total_premium FROM wealth_segment_pivot WHERE market = 'PHKL' GROUP BY new_or_existing",
        "notes": "Compare New vs Existing within a market",
    },
    {
        "question": "Show me new customer count by wealth segment across all markets.",
        "sql": "SELECT market, wealth_segment, SUM(customer_count) AS total_customers, SUM(annual_premium) AS total_premium FROM wealth_segment_pivot WHERE new_or_existing = 'New' GROUP BY market, wealth_segment ORDER BY market, wealth_segment",
        "notes": "Filter to New customers, then multi-dimension group",
    },
    # ── Pattern: Proportion / percentage ──
    {
        "question": "What percentage of customers are HNW in each market?",
        "sql": "SELECT market, SUM(CASE WHEN wealth_segment = 'High-net-worth' THEN customer_count ELSE 0 END) * 1.0 / SUM(customer_count) AS hnw_pct FROM wealth_segment_pivot GROUP BY market ORDER BY market",
        "notes": "Proportion calculation using CASE WHEN inside SUM. Multiply by 1.0 for float division.",
    },
    {
        "question": "What is the HNW premium share in PHKL?",
        "sql": "SELECT SUM(CASE WHEN wealth_segment = 'High-net-worth' THEN annual_premium ELSE 0 END) * 1.0 / SUM(annual_premium) AS hnw_premium_share FROM wealth_segment_pivot WHERE market = 'PHKL'",
        "notes": "Single-market proportion — no GROUP BY since only one market in WHERE",
    },
    # ── Pattern: Product holding rate ──
    {
        "question": "What percentage of customers hold medical insurance in each market?",
        "sql": "SELECT market, SUM(CASE WHEN medical_holding = 'Yes' THEN customer_count ELSE 0 END) * 1.0 / SUM(customer_count) AS medical_holding_rate FROM wealth_segment_pivot GROUP BY market ORDER BY market",
        "notes": "Product holding rate — proportion of customers with medical_holding = 'Yes'",
    },
    {
        "question": "Show me the investment holding rate by wealth segment in PAMB.",
        "sql": "SELECT wealth_segment, SUM(CASE WHEN investment_holding = 'Yes' THEN customer_count ELSE 0 END) * 1.0 / SUM(customer_count) AS investment_rate FROM wealth_segment_pivot WHERE market = 'PAMB' GROUP BY wealth_segment",
        "notes": "Holding rate filtered by market, grouped by segment",
    },
    # ── Pattern: Multi-condition filter ──
    {
        "question": "How many matured family with kid customers in the Affluent segment hold both savings and medical products in PHKL?",
        "sql": "SELECT SUM(customer_count) AS total_customers, SUM(annual_premium) AS total_premium FROM wealth_segment_pivot WHERE market = 'PHKL' AND wealth_segment = 'Affluent' AND life_stage = 'matured family with kid' AND saving_holding = 'Yes' AND medical_holding = 'Yes'",
        "notes": "Multiple WHERE conditions — narrow down to a specific customer group",
    },
    # ── Pattern: Top N / ORDER BY ──
    {
        "question": "Which market has the highest total premium?",
        "sql": "SELECT market, SUM(annual_premium) AS total_premium, SUM(customer_count) AS total_customers FROM wealth_segment_pivot GROUP BY market ORDER BY total_premium DESC",
        "notes": "Ranking — ORDER BY the aggregated metric DESC",
    },
    {
        "question": "Show me the top 3 markets by customer count.",
        "sql": "SELECT market, SUM(customer_count) AS total_customers FROM wealth_segment_pivot GROUP BY market ORDER BY total_customers DESC LIMIT 3",
        "notes": "Top N with LIMIT after ORDER BY DESC",
    },
    # ── Pattern: Tenure-based analysis ──
    {
        "question": "What is the average premium per customer by tenure in PLUK?",
        "sql": "SELECT customer_tenure, SUM(customer_count) AS total_customers, SUM(annual_premium) AS total_premium, SUM(annual_premium) / SUM(customer_count) AS avg_premium FROM wealth_segment_pivot WHERE market = 'PLUK' GROUP BY customer_tenure ORDER BY customer_tenure",
        "notes": "Calculated metric: SUM(premium) / SUM(customers) per tenure band",
    },
    # ── Pattern: Golden age / senior segment ──
    {
        "question": "How many golden age customers do we have across all markets, and what is their premium contribution?",
        "sql": "SELECT market, SUM(customer_count) AS total_customers, SUM(annual_premium) AS total_premium FROM wealth_segment_pivot WHERE life_stage = 'golden age' GROUP BY market ORDER BY total_premium DESC",
        "notes": "Filter to one life_stage value, compare across markets, ranked by premium",
    },
]

# ═══════════════════════════════════════════════════════════════════════
# PROMPT BUILDER
# ═══════════════════════════════════════════════════════════════════════

def build_system_prompt() -> str:
    """Build the system prompt with schema, glossary, synonyms, and examples."""
    glossary_text = "\n".join(
        f"- {c['column']} ({c['type']}): {c['description']}. "
        f"Possible values: {c['values']}"
        for c in COLUMN_GLOSSARY
    )

    synonym_text = build_synonym_rules()

    examples_text = (
        "\n".join(
            f"Q: {ex['question']}\nSQL: {ex['sql']}"
            for ex in FEW_SHOT_EXAMPLES
        )
        if FEW_SHOT_EXAMPLES
        else "(No examples yet — add in FEW_SHOT_EXAMPLES)"
    )

    prompt = f"""You are a SQL assistant for a life insurance customer analytics database.

The database has ONE table:

Table: {TABLE_NAME}
{SCHEMA_DDL}

Column glossary:
{glossary_text}

{synonym_text}

Key formulas:
- Total customers: {KPI_FORMULAS['total_customers']}
- Total premium: {KPI_FORMULAS['total_premium']}
- Average premium per customer: {KPI_FORMULAS['avg_premium_per_customer']}
- Wealth segment proportion: {KPI_FORMULAS['wealth_segment_proportion']}
- Product holding rate: {KPI_FORMULAS['product_holding_rate']}

Rules:
1. Use exact column names from the glossary. Apply synonym mappings first.
2. Use exact column VALUES from the glossary. Apply value synonym mappings first.
   For example: "HNW" → "High-net-worth", "LBU" → "market"
3. customer_count and annual_premium are aggregated measures — always use SUM().
4. For proportions, divide the subset SUM by the total SUM.
5. Filter with WHERE before aggregating unless the question asks for totals.
6. Output ONLY the SQL query, nothing else. No markdown, no explanation.

Example Q&A pairs:
{examples_text}
"""
    return prompt
