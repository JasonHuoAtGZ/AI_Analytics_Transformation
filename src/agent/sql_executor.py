"""SQL Executor — validates and executes SQL against DuckDB.

Enforces safety rules:
- SELECT-only (no INSERT/UPDATE/DELETE/DROP/ALTER)
- Read-only access
"""

import re

import pandas as pd

from src.db.connection import db

FORBIDDEN_KEYWORDS: list[str] = [
    "INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "CREATE",
    "TRUNCATE", "GRANT", "REVOKE", "EXEC", "EXECUTE",
]


class SQLValidationError(Exception):
    """Raised when generated SQL fails validation or execution."""


class SQLExecutor:
    """Validates and executes SQL queries against DuckDB."""

    def validate(self, sql: str) -> None:
        """Validate SQL for safety.

        Checks for forbidden keywords (write operations) and
        verifies the query references the correct table.
        """
        sql_upper = sql.upper()

        # ── Check 1: No forbidden keywords ──
        for kw in FORBIDDEN_KEYWORDS:
            if re.search(rf"\b{kw}\b", sql_upper):
                raise SQLValidationError(
                    f"Forbidden keyword detected: {kw}. Only SELECT queries are allowed."
                )

        # ── Check 2: Must contain SELECT ──
        if "SELECT" not in sql_upper:
            raise SQLValidationError("SQL must be a SELECT query.")

        # ── Check 3: Must reference the correct table ──
        if "wealth_segment_pivot" not in sql.lower():
            raise SQLValidationError(
                "Query must reference the wealth_segment_pivot table."
            )

    def execute(self, sql: str) -> pd.DataFrame:
        """Validate and execute a SQL query, returning results as a DataFrame.

        Validation covers safety rules (no write operations).
        DuckDB itself validates column/table existence — if the LLM
        generates an invalid column name, DuckDB will raise a clear error.
        """
        self.validate(sql)
        try:
            return db.query(sql)
        except Exception as e:
            raise SQLValidationError(f"DuckDB error: {e}") from e


# Singleton instance
executor = SQLExecutor()
