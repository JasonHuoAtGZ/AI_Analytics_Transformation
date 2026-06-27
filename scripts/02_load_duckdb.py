"""Load wealth_segment_pivot.xlsx into DuckDB.

Reads the generated Excel file and creates a DuckDB table for querying.
"""

from pathlib import Path
import sys

import duckdb
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from environment.config import settings

# ── Paths ───────────────────────────────────────────────────────────────
EXCEL_PATH = Path("data/generated/wealth_segment_pivot.xlsx")
DB_PATH = settings.duckdb.path

# ── Read Excel ──────────────────────────────────────────────────────────
print(f"Reading: {EXCEL_PATH}")
df = pd.read_excel(EXCEL_PATH, engine="openpyxl")
print(f"  Rows: {len(df):,}")
print(f"  Columns: {list(df.columns)}")

# ── Connect & create table ──────────────────────────────────────────────
DB_PATH.parent.mkdir(parents=True, exist_ok=True)
con = duckdb.connect(str(DB_PATH))

# Drop existing table if re-running
con.execute("DROP TABLE IF EXISTS wealth_segment_pivot")

# Create table with appropriate types
con.execute("""
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
""")

# ── Insert data ─────────────────────────────────────────────────────────
con.execute("INSERT INTO wealth_segment_pivot SELECT * FROM df")
con.close()

# ── Verify ──────────────────────────────────────────────────────────────
con = duckdb.connect(str(DB_PATH))
row_count = con.execute("SELECT COUNT(*) FROM wealth_segment_pivot").fetchone()[0]
sample = con.execute("SELECT * FROM wealth_segment_pivot LIMIT 3").fetchdf()
con.close()

print(f"\nDB path: {DB_PATH.resolve()}")
print(f"DB size: {DB_PATH.stat().st_size / 1_048_576:.1f} MB")
print(f"Table rows: {row_count:,}")
print(f"Sample columns: {list(sample.columns)}")
print("\nDone — wealth_segment_pivot loaded into DuckDB.")
