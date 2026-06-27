"""End-to-end integration test for Phase 3 — Query Engine pipeline."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.agent.query_engine import query_engine
from src.agent.sql_executor import executor, SQLValidationError
from src.agent.response_formatter import formatter


def test(question: str, label: str = "") -> None:
    print(f"\n{'='*60}")
    print(f"  {label or question}")
    print(f"{'='*60}")
    try:
        sql = query_engine.generate_sql(question)
        print(f"  SQL: {sql}")
        result = executor.execute(sql)
        resp = formatter.format(question, sql, result)
        print(f"  Rows: {resp['row_count']}")
        print(f"  Summary: {resp['summary']}")
        if resp["row_count"] <= 5:
            print(f"  Data:\n{resp['table'].to_string(index=False)}")
    except SQLValidationError as e:
        print(f"  VALIDATION ERROR: {e}")
    except Exception as e:
        print(f"  ERROR: {e}")


# Simple total
test("How many customers do we have in total?", "Simple total")

# HNW by market
test("How many HNW customers does each market have?", "HNW by market")

# Filtered & grouped
test("Show me customer count by wealth segment in PHKL.", "PHKL segment breakdown")
