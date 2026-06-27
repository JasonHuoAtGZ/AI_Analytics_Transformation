"""Knowledge base for the Customer Analytics Query Agent.

This module defines the table schema, column glossary, synonym mappings,
KPI formulas, and few-shot examples that ground the LLM when generating SQL.
"""

# ¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T
# TABLE SCHEMA
# ¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T

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

# ¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T
# COLUMN GLOSSARY
# ¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T

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
        "description": "Customer wealth tier â used for proportion calculations",
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

# ¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T
# SYNONYMS
# ¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T

COLUMN_SYNONYMS: dict[str, str] = {
    # ©¤©¤ market ©¤©¤
    "LBU": "market",
    "lbu": "market",
    "local market": "market",
    "local business unit": "market",
    "business unit": "market",
    "entity": "market",
    "market code": "market",
    "country": "market",
    # ©¤©¤ wealth_segment ©¤©¤
    "segment": "wealth_segment",
    "customer segment": "wealth_segment",
    "customer tier": "wealth_segment",
    "wealth tier": "wealth_segment",
    "wealth band": "wealth_segment",
    "customer band": "wealth_segment",
    # ©¤©¤ customer_tenure ©¤©¤
    "tenure": "customer_tenure",
    "years with us": "customer_tenure",
    "relationship length": "customer_tenure",
    "customer age": "customer_tenure",
    "tenure band": "customer_tenure",
    # ©¤©¤ customer_count ©¤©¤
    "number of customers": "customer_count",
    "customer base": "customer_count",
    "customer volume": "customer_count",
    "policy count": "customer_count",
    "count of customers": "customer_count",
    "customer numbers": "customer_count",
    "how many customers": "customer_count",
    # ©¤©¤ annual_premium ©¤©¤
    "premium": "annual_premium",
    "APE": "annual_premium",
    "annual premium equivalent": "annual_premium",
    "revenue": "annual_premium",
    "premium income": "annual_premium",
    "premium volume": "annual_premium",
    "GWP": "annual_premium",
    "gross written premium": "annual_premium",
    # ©¤©¤ life_stage ©¤©¤
    "life cycle": "life_stage",
    "demographic": "life_stage",
    "life stage group": "life_stage",
    # ©¤©¤ new_or_existing ©¤©¤
    "customer type": "new_or_existing",
    "new vs existing": "new_or_existing",
    "acquisition type": "new_or_existing",
    "new customer": "new_or_existing",
    "existing customer": "new_or_existing",
    # ©¤©¤ holding columns ©¤©¤
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
    # ©¤©¤ wealth_segment values ©¤©¤
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
    # ©¤©¤ new_or_existing values ©¤©¤
    "new business": "New",
    "newly acquired": "New",
    "new customer": "New",
    "existing customer": "Existing",
    "in-force": "Existing",
    "renewal": "Existing",
    # ©¤©¤ tenure values ©¤©¤
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
    rules.append("SYNONYM RULES â when the user mentions any of these, use the mapped term:\n")
    rules.append("Column synonyms (term â actual column name):")
    for syn, col in sorted(COLUMN_SYNONYMS.items()):
        rules.append(f'  "{syn}" â {col}')
    rules.append("\nValue synonyms (term â actual column value):")
    for syn, val in sorted(VALUE_SYNONYMS.items()):
        rules.append(f'  "{syn}" â {val}')
    return "\n".join(rules)


# ¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T
# KPI FORMULAS
# ¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T

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

# ¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T
# FEW-SHOT EXAMPLES
# ¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T¨T

FEW_SHOT_EXAMPLES: list[dict] = [
    {

    # -- Pattern: Simple aggregation by one dimension --
        "question": "How many customers do we have in total?",
        "sql": "SELECT SUM(customer_count) AS total_customers FROM wealth_segment_pivot",
        "reasoning": "A simple grand total across all dimensions. No filters or groupings needed -- just SUM the customer_count column.",
        "chart_type": "none",
        "notes": "Simple total \u00e2\u0080\u0094 no GROUP BY needed"
    },
    {
        "question": "What is the total annual premium across all markets?",
        "sql": "SELECT SUM(annual_premium) AS total_premium FROM wealth_segment_pivot",
        "reasoning": "Grand total of annual_premium. Single number answer -- no grouping needed since we are summing everything.",
        "chart_type": "none",
        "notes": "Simple total of annual_premium"
    },
    {
        "question": "Show me customer count by wealth segment.",
        "sql": "SELECT wealth_segment, SUM(customer_count) AS total_customers, SUM(annual_premium) AS total_premium FROM wealth_segment_pivot GROUP BY wealth_segment",
        "reasoning": "Compare the three wealth segments (HNW, Affluent, Mass) side by side. Include both customer count and premium for a complete picture.",
        "chart_type": "bar",
        "notes": "Group by one dimension \u00e2\u0080\u0094 always include both metrics for completeness"
    },
    {

    # -- Pattern: Filter by market, group by one dimension --
        "question": "What is the customer breakdown by wealth segment in PHKL?",
        "sql": "SELECT wealth_segment, SUM(customer_count) AS total_customers, SUM(annual_premium) AS total_premium FROM wealth_segment_pivot WHERE market = 'PHKL' GROUP BY wealth_segment",
        "reasoning": "Drill down into PHKL specifically. Filter to one market, then see how customers and premium split across the three wealth segments.",
        "chart_type": "bar",
        "notes": "WHERE before GROUP BY \u00e2\u0080\u0094 filter to one market, then aggregate"
    },
    {
        "question": "Show me the premium by life stage for PACS.",
        "sql": "SELECT life_stage, SUM(customer_count) AS total_customers, SUM(annual_premium) AS total_premium FROM wealth_segment_pivot WHERE market = 'PACS' GROUP BY life_stage",
        "reasoning": "Life stage breakdown for PACS market. Group by life_stage to see how premium distributes across the customer lifecycle.",
        "chart_type": "bar",
        "notes": "Single-market filter with different grouping dimension"
    },
    {

    # -- Pattern: Filter by segment, group by market (cross-market comparison) --
        "question": "How many HNW customers does each market have?",
        "sql": "SELECT market, SUM(customer_count) AS total_customers, SUM(annual_premium) AS total_premium FROM wealth_segment_pivot WHERE wealth_segment = 'High-net-worth' GROUP BY market",
        "reasoning": "Apply synonym: HNW maps to High-net-worth. Filter to only HNW customers, then compare across all 10 markets to see which markets have the largest high-value customer bases.",
        "chart_type": "bar",
        "notes": "Apply value synonym: HNW \u00e2\u0080\u0094 High-net-worth. Filter to one segment, compare across markets."
    },
    {
        "question": "Compare the Affluent segment customer count and premium across all LBUs.",
        "sql": "SELECT market, SUM(customer_count) AS total_customers, SUM(annual_premium) AS total_premium FROM wealth_segment_pivot WHERE wealth_segment = 'Affluent' GROUP BY market ORDER BY market",
        "reasoning": "Apply synonym: LBU maps to market. Cross-market comparison of the Affluent segment -- ordered alphabetically for easy side-by-side reading.",
        "chart_type": "bar",
        "notes": "Apply synonym: LBU \u00e2\u0080\u0094 market. ORDER BY for clean comparison."
    },
    {

    # -- Pattern: Multi-dimension grouping --
        "question": "Show me customer count by wealth segment and life stage for PHKL.",
        "sql": "SELECT wealth_segment, life_stage, SUM(customer_count) AS total_customers, SUM(annual_premium) AS total_premium FROM wealth_segment_pivot WHERE market = 'PHKL' GROUP BY wealth_segment, life_stage ORDER BY wealth_segment, life_stage",
        "reasoning": "A matrix view for PHKL: rows are wealth segments, columns are life stages. This shows the full customer composition of one market in a single query.",
        "chart_type": "bar",
        "notes": "Two GROUP BY dimensions for a matrix view"
    },
    {
        "question": "Break down customer count by market and customer tenure.",
        "sql": "SELECT market, customer_tenure, SUM(customer_count) AS total_customers FROM wealth_segment_pivot GROUP BY market, customer_tenure ORDER BY market, customer_tenure",
        "reasoning": "Cross-market heatmap: how does customer tenure distribution vary by market? Which markets have more long-tenure vs newer customers?",
        "chart_type": "bar",
        "notes": "Cross-market comparison with tenure breakout"
    },
    {

    # -- Pattern: New vs Existing comparison --
        "question": "How do new customers compare to existing customers in terms of premium in PHKL?",
        "sql": "SELECT new_or_existing, SUM(customer_count) AS total_customers, SUM(annual_premium) AS total_premium FROM wealth_segment_pivot WHERE market = 'PHKL' GROUP BY new_or_existing",
        "reasoning": "Head-to-head comparison of New vs Existing customers within PHKL. This reveals whether new business or the existing book drives more premium.",
        "chart_type": "bar",
        "notes": "Compare New vs Existing within a market"
    },
    {
        "question": "Show me new customer count by wealth segment across all markets.",
        "sql": "SELECT market, wealth_segment, SUM(customer_count) AS total_customers, SUM(annual_premium) AS total_premium FROM wealth_segment_pivot WHERE new_or_existing = 'New' GROUP BY market, wealth_segment ORDER BY market, wealth_segment",
        "reasoning": "Focus on new customers only, then break down by market and wealth segment. This reveals which markets are acquiring which types of customers.",
        "chart_type": "bar",
        "notes": "Filter to New customers, then multi-dimension group"
    },
    {

    # -- Pattern: Proportion / percentage --
        "question": "What percentage of customers are HNW in each market?",
        "sql": "SELECT market, SUM(CASE WHEN wealth_segment = 'High-net-worth' THEN customer_count ELSE 0 END) * 1.0 / SUM(customer_count) AS hnw_pct FROM wealth_segment_pivot GROUP BY market ORDER BY market",
        "reasoning": "Calculate HNW penetration rate per market: what share of each market total customers are High-net-worth. Use CASE WHEN to isolate HNW count, divide by total.",
        "chart_type": "bar",
        "notes": "Proportion calculation using CASE WHEN inside SUM. Multiply by 1.0 for float division."
    },
    {
        "question": "What is the HNW premium share in PHKL?",
        "sql": "SELECT SUM(CASE WHEN wealth_segment = 'High-net-worth' THEN annual_premium ELSE 0 END) * 1.0 / SUM(annual_premium) AS hnw_premium_share FROM wealth_segment_pivot WHERE market = 'PHKL'",
        "reasoning": "HNW premium concentration within PHKL: what fraction of PHKL total premium comes from the HNW segment. Single-market, single-number output.",
        "chart_type": "none",
        "notes": "Single-market proportion \u00e2\u0080\u0094 no GROUP BY since only one market in WHERE"
    },
    {

    # -- Pattern: Product holding rate --
        "question": "What percentage of customers hold medical insurance in each market?",
        "sql": "SELECT market, SUM(CASE WHEN medical_holding = 'Yes' THEN customer_count ELSE 0 END) * 1.0 / SUM(customer_count) AS medical_holding_rate FROM wealth_segment_pivot GROUP BY market ORDER BY market",
        "reasoning": "Medical insurance penetration by market. Which markets have the highest medical product attachment rates?",
        "chart_type": "bar",
        "notes": "Product holding rate \u00e2\u0080\u0094 proportion of customers with medical_holding = 'Yes'"
    },
    {
        "question": "Show me the investment holding rate by wealth segment in PAMB.",
        "sql": "SELECT wealth_segment, SUM(CASE WHEN investment_holding = 'Yes' THEN customer_count ELSE 0 END) * 1.0 / SUM(customer_count) AS investment_rate FROM wealth_segment_pivot WHERE market = 'PAMB' GROUP BY wealth_segment",
        "reasoning": "Investment product penetration within PAMB, broken down by wealth segment. Expect higher rates in HNW and Affluent vs Mass.",
        "chart_type": "bar",
        "notes": "Holding rate filtered by market, grouped by segment"
    },
    {

    # -- Pattern: Multi-condition filter --
        "question": "How many matured family with kid customers in the Affluent segment hold both savings and medical products in PHKL?",
        "sql": "SELECT SUM(customer_count) AS total_customers, SUM(annual_premium) AS total_premium FROM wealth_segment_pivot WHERE market = 'PHKL' AND wealth_segment = 'Affluent' AND life_stage = 'matured family with kid' AND saving_holding = 'Yes' AND medical_holding = 'Yes'",
        "reasoning": "Very specific customer cohort: PHKL, Affluent, matured family with kids, holding both savings and medical. Multiple AND conditions narrow to this exact group.",
        "chart_type": "none",
        "notes": "Multiple WHERE conditions \u00e2\u0080\u0094 narrow down to a specific customer group"
    },
    {

    # -- Pattern: Top N / ORDER BY --
        "question": "Which market has the highest total premium?",
        "sql": "SELECT market, SUM(annual_premium) AS total_premium, SUM(customer_count) AS total_customers FROM wealth_segment_pivot GROUP BY market ORDER BY total_premium DESC",
        "reasoning": "Rank all 10 markets by total premium descending. The top row is the answer, but showing all markets provides the full competitive landscape.",
        "chart_type": "bar",
        "notes": "Ranking \u00e2\u0080\u0094 ORDER BY the aggregated metric DESC"
    },
    {
        "question": "Show me the top 3 markets by customer count.",
        "sql": "SELECT market, SUM(customer_count) AS total_customers FROM wealth_segment_pivot GROUP BY market ORDER BY total_customers DESC LIMIT 3",
        "reasoning": "Top 3 ranking by customer volume. LIMIT 3 after ORDER BY DESC gives just the top performers.",
        "chart_type": "bar",
        "notes": "Top N with LIMIT after ORDER BY DESC"
    },
    {

    # -- Pattern: Tenure-based analysis --
        "question": "What is the average premium per customer by tenure in PLUK?",
        "sql": "SELECT customer_tenure, SUM(customer_count) AS total_customers, SUM(annual_premium) AS total_premium, SUM(annual_premium) / SUM(customer_count) AS avg_premium FROM wealth_segment_pivot WHERE market = 'PLUK' GROUP BY customer_tenure ORDER BY customer_tenure",
        "reasoning": "How premium per customer evolves with tenure in PLUK. Calculate avg_premium per tenure band. Ordered by tenure for a natural progression -- line chart best captures this trend.",
        "chart_type": "line",
        "notes": "Calculated metric: SUM(premium) / SUM(customers) per tenure band"
    },
    {

    # -- Pattern: Golden age / senior segment --
        "question": "How many golden age customers do we have across all markets, and what is their premium contribution?",
        "sql": "SELECT market, SUM(customer_count) AS total_customers, SUM(annual_premium) AS total_premium FROM wealth_segment_pivot WHERE life_stage = 'golden age' GROUP BY market ORDER BY total_premium DESC",
        "reasoning": "Senior customer segment analysis: filter to golden age, then compare across markets ranked by premium. Shows which markets have the strongest senior customer base.",
        "chart_type": "bar",
        "notes": "Filter to one life_stage value, compare across markets, ranked by premium"
    },
    {

    # -- Pattern: Proportion + ranking --
        "question": "Which market has the highest HNW customer share?",
        "sql": "SELECT market, SUM(CASE WHEN wealth_segment = 'High-net-worth' THEN customer_count ELSE 0 END) * 1.0 / SUM(customer_count) AS hnw_pct, SUM(customer_count) AS total_customers FROM wealth_segment_pivot GROUP BY market ORDER BY hnw_pct DESC LIMIT 1",
        "reasoning": "HNW premium concentration within PHKL: what fraction of PHKL total premium comes from the HNW segment. Single-market, single-number output.",
        "chart_type": "none",
        "notes": "Proportion calculation with ranking -- ORDER BY the calculated column DESC + LIMIT 1"
    },
    {

    # -- Pattern: Cross-segment comparison with calculated metric --
        "question": "Compare average premium per customer: HNW vs Mass in each market.",
        "sql": "SELECT market, SUM(CASE WHEN wealth_segment = 'High-net-worth' THEN annual_premium ELSE 0 END) / NULLIF(SUM(CASE WHEN wealth_segment = 'High-net-worth' THEN customer_count ELSE 0 END), 0) AS hnw_avg_premium, SUM(CASE WHEN wealth_segment = 'Mass' THEN annual_premium ELSE 0 END) / NULLIF(SUM(CASE WHEN wealth_segment = 'Mass' THEN customer_count ELSE 0 END), 0) AS mass_avg_premium FROM wealth_segment_pivot GROUP BY market ORDER BY market",
        "reasoning": "Very specific customer cohort: PHKL, Affluent, matured family with kids, holding both savings and medical. Multiple AND conditions narrow to this exact group. Single-number output.",
        "chart_type": "none",
        "notes": "Pivot-style comparison -- each row shows two segments side by side for easy visual comparison"
    },
    {

    # -- Pattern: Multi-product holder count --
        "question": "How many customers hold 3 or more products in PHKL?",
        "sql": "SELECT SUM(customer_count) AS total_customers, SUM(annual_premium) AS total_premium FROM wealth_segment_pivot WHERE market = 'PHKL' AND (CASE WHEN saving_holding = 'Yes' THEN 1 ELSE 0 END + CASE WHEN investment_holding = 'Yes' THEN 1 ELSE 0 END + CASE WHEN medical_holding = 'Yes' THEN 1 ELSE 0 END + CASE WHEN critical_illness_holding = 'Yes' THEN 1 ELSE 0 END + CASE WHEN others_health_and_protection_holding = 'Yes' THEN 1 ELSE 0 END) >= 3",
        "reasoning": "A simple grand total across all dimensions. No filters or groupings needed -- just SUM the customer_count column.",
        "chart_type": "none",
        "notes": "Multi-condition derived from multiple flag columns -- use CASE WHEN to convert Yes/No to 1/0 and sum"
    },
    {

    # -- Pattern: Threshold filter on calculated metric --
        "question": "Which markets have a medical holding rate above 50%?",
        "sql": "SELECT market, SUM(CASE WHEN medical_holding = 'Yes' THEN customer_count ELSE 0 END) * 1.0 / SUM(customer_count) AS medical_holding_rate, SUM(customer_count) AS total_customers FROM wealth_segment_pivot GROUP BY market HAVING SUM(CASE WHEN medical_holding = 'Yes' THEN customer_count ELSE 0 END) * 1.0 / SUM(customer_count) > 0.5 ORDER BY medical_holding_rate DESC",
        "reasoning": "How premium per customer evolves with tenure in PLUK. Calculate avg_premium per tenure band. Ordered by tenure for a natural progression -- line chart best shows this trend.",
        "chart_type": "line",
        "notes": "HAVING clause for post-aggregation filtering on a calculated proportion"
    },
    {

    # -- Pattern: Vague question -- default to wealth segment breakdown --
        "question": "How is PHKL performing?",
        "sql": "SELECT wealth_segment, SUM(customer_count) AS total_customers, SUM(annual_premium) AS total_premium FROM wealth_segment_pivot WHERE market = 'PHKL' GROUP BY wealth_segment ORDER BY total_premium DESC",
        "reasoning": "Vague performance question -- default to the standard market overview: customer count and premium by wealth segment, ranked by premium. This gives a complete picture of the market's composition.",
        "chart_type": "bar",
        "notes": "Default handling for ambiguous questions -- provide a wealth segment breakdown as the most informative single view"
    },
    {

    # -- Pattern: Multiple holding rates side by side --
        "question": "What is the product holding mix in the Mass segment across markets?",
        "sql": "SELECT market, SUM(CASE WHEN saving_holding = 'Yes' THEN customer_count ELSE 0 END) * 1.0 / SUM(customer_count) AS saving_rate, SUM(CASE WHEN investment_holding = 'Yes' THEN customer_count ELSE 0 END) * 1.0 / SUM(customer_count) AS investment_rate, SUM(CASE WHEN medical_holding = 'Yes' THEN customer_count ELSE 0 END) * 1.0 / SUM(customer_count) AS medical_rate, SUM(CASE WHEN critical_illness_holding = 'Yes' THEN customer_count ELSE 0 END) * 1.0 / SUM(customer_count) AS ci_rate, SUM(CASE WHEN others_health_and_protection_holding = 'Yes' THEN customer_count ELSE 0 END) * 1.0 / SUM(customer_count) AS other_rate FROM wealth_segment_pivot WHERE wealth_segment = 'Mass' GROUP BY market ORDER BY market",
        "reasoning": "Product holding mix = all 5 holding rates in one view. Filter to Mass segment, compute each holding rate as a separate column for easy side-by-side comparison across markets.",
        "chart_type": "bar",
        "notes": "Multiple calculated metrics in one query -- each product type gets its own column, ideal for grouped bar chart"
    },
    {

    # -- Pattern: Multi-filter with cross-market comparison --
        "question": "How many new customers are in the young single life stage across markets?",
        "sql": "SELECT market, SUM(customer_count) AS total_customers, SUM(annual_premium) AS total_premium FROM wealth_segment_pivot WHERE new_or_existing = 'New' AND life_stage = 'young single' GROUP BY market ORDER BY total_customers DESC",
        "reasoning": "Two independent filters (new customers + young single life stage) combined with AND, then compare across markets ranked by customer count.",
        "chart_type": "bar",
        "notes": "Multiple WHERE filters with cross-market comparison -- ranked by customer count for easy prioritization"
    },
    {

    # -- Pattern: Segment-filtered ranking --
        "question": "Which tenure band generates the highest premium in the Affluent segment?",
        "sql": "SELECT customer_tenure, SUM(customer_count) AS total_customers, SUM(annual_premium) AS total_premium FROM wealth_segment_pivot WHERE wealth_segment = 'Affluent' GROUP BY customer_tenure ORDER BY total_premium DESC",
        "reasoning": "Filter to Affluent segment, group by tenure band, rank by premium descending to find the highest-value tenure group within the Affluent segment.",
        "chart_type": "bar",
        "notes": "Segment-filtered ranking -- narrow to one wealth segment then rank by metric across tenure bands"
    },
    {

    # -- Pattern: Top N with proportion --
        "question": "Show me the top 5 markets by HNW customer proportion.",
        "sql": "SELECT market, SUM(CASE WHEN wealth_segment = 'High-net-worth' THEN customer_count ELSE 0 END) * 1.0 / SUM(customer_count) AS hnw_pct, SUM(customer_count) AS total_customers FROM wealth_segment_pivot GROUP BY market ORDER BY hnw_pct DESC LIMIT 5",
        "reasoning": "Top 5 ranking by a calculated proportion. Include total_customers for context -- a high HNW percentage on a tiny customer base is less meaningful than on a large one.",
        "chart_type": "bar",
        "notes": "Proportion-based ranking with LIMIT -- always include the base metric for context"
    },
    {

    # -- Pattern: Single-market all-holding-rates snapshot --
        "question": "Show me the holding rates for all 5 product types in PHKL.",
        "sql": "SELECT SUM(CASE WHEN saving_holding = 'Yes' THEN customer_count ELSE 0 END) * 1.0 / SUM(customer_count) AS saving_rate, SUM(CASE WHEN investment_holding = 'Yes' THEN customer_count ELSE 0 END) * 1.0 / SUM(customer_count) AS investment_rate, SUM(CASE WHEN medical_holding = 'Yes' THEN customer_count ELSE 0 END) * 1.0 / SUM(customer_count) AS medical_rate, SUM(CASE WHEN critical_illness_holding = 'Yes' THEN customer_count ELSE 0 END) * 1.0 / SUM(customer_count) AS ci_rate, SUM(CASE WHEN others_health_and_protection_holding = 'Yes' THEN customer_count ELSE 0 END) * 1.0 / SUM(customer_count) AS other_rate FROM wealth_segment_pivot WHERE market = 'PHKL'",
        "reasoning": "Single-market product penetration snapshot -- all 5 holding rates in one row for quick visual comparison. No GROUP BY needed since only one market in WHERE.",
        "chart_type": "bar",
        "notes": "Single-row multi-metric output -- 5 calculated rates for one market, ideal for a horizontal bar chart comparison"
    },
]

# =============================================================================
# PROMPT BUILDER
# =============================================================================

def build_system_prompt() -> str:
    """Build the system prompt with persona, schema, glossary, synonyms, rules, and examples."""
    glossary_text = "\n".join(
        f"- {c['column']} ({c['type']}): {c['description']}. "
        f"Possible values: {c['values']}"
        for c in COLUMN_GLOSSARY
    )

    synonym_text = build_synonym_rules()

    examples_text = (
        "\n\n".join(
            f"Q: {ex['question']}\nREASONING: {ex.get('reasoning', '')}\nSQL: {ex['sql']}\nCHART_TYPE: {ex.get('chart_type', 'bar')}"
            for ex in FEW_SHOT_EXAMPLES
        )
        if FEW_SHOT_EXAMPLES
        else "(No examples yet -- add in FEW_SHOT_EXAMPLES)"
    )

    prompt = f"""You are a senior business analyst with 10+ years of experience at a life insurance company. You are deeply familiar with customer analytics, distribution channels, and insurance KPIs. You answer business questions by writing SQL against the company\'s customer analytics database.

Your audience is product managers and distribution heads. Write clean, efficient DuckDB SQL.

## DATABASE SCHEMA

The database has ONE table:

Table: {TABLE_NAME}
{SCHEMA_DDL}

## COLUMN GLOSSARY

{glossary_text}

{synonym_text}

## KEY FORMULAS

- Total customers: {KPI_FORMULAS['total_customers']}
- Total premium: {KPI_FORMULAS['total_premium']}
- Average premium per customer: {KPI_FORMULAS['avg_premium_per_customer']}
- Wealth segment proportion: {KPI_FORMULAS['wealth_segment_proportion']}
- Product holding rate: {KPI_FORMULAS['product_holding_rate']}

## OUTPUT FORMAT

Respond with ONLY the SQL query wrapped in a fenced code block. Do not include any other text, tables, or explanations.

Example output:
`sql
SELECT market, SUM(customer_count) AS total_customers
FROM wealth_segment_pivot
GROUP BY market
ORDER BY total_customers DESC
`

## SQL RULES

1. Apply synonyms first: "HNW" = wealth_segment = \'High-net-worth\', "LBU" = market, etc.
2. customer_count and annual_premium are pre-aggregated -- always wrap with SUM().
3. Proportions: SUM(CASE WHEN condition THEN customer_count ELSE 0 END) * 1.0 / SUM(customer_count)
4. Filter with WHERE before GROUP BY unless asking for totals.
5. Vague questions: default to customer count + premium by wealth segment, ordered by premium DESC.
6. "Compare" questions: include both entities, add difference/ratio where insightful.
7. Always ORDER BY the most relevant metric DESC unless specified otherwise.
8. "Top N" questions: ORDER BY ... DESC LIMIT N.
9. Include BOTH customer_count and annual_premium in SELECT when grouping by any dimension.

## FEW-SHOT EXAMPLES

{examples_text}
"""
    return prompt