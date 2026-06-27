"""DuckDB connection manager for the Customer Analytics Query Agent.

Provides a single connection point to the DuckDB database.
On first connect, ensures the database file exists.
"""

from pathlib import Path
from typing import Optional

import duckdb
import pandas as pd

from environment.config import settings


class DuckDBConnection:
    """Manages a DuckDB connection to the customer analytics database."""

    def __init__(self) -> None:
        self._con: Optional[duckdb.DuckDBPyConnection] = None
        self._db_path: Path = settings.duckdb.path

    @property
    def db_path(self) -> Path:
        return self._db_path

    def connect(self) -> duckdb.DuckDBPyConnection:
        """Return a DuckDB connection, creating one if needed."""
        if self._con is None:
            self._db_path.parent.mkdir(parents=True, exist_ok=True)
            self._con = duckdb.connect(str(self._db_path))
        return self._con

    def query(self, sql: str) -> pd.DataFrame:
        """Execute a SELECT query and return results as a DataFrame."""
        con = self.connect()
        return con.execute(sql).fetchdf()

    def table_exists(self, table_name: str) -> bool:
        """Check if a table exists in the database."""
        con = self.connect()
        result = con.execute(
            "SELECT COUNT(*) FROM information_schema.tables WHERE table_name = ?",
            [table_name],
        ).fetchone()
        return result[0] > 0

    def get_columns(self, table_name: str) -> list[dict]:
        """Return column metadata for a table: name, type."""
        con = self.connect()
        return con.execute(
            "SELECT column_name, data_type FROM information_schema.columns "
            "WHERE table_name = ? ORDER BY ordinal_position",
            [table_name],
        ).fetchdf().to_dict("records")

    def close(self) -> None:
        if self._con is not None:
            self._con.close()
            self._con = None


# Singleton instance for the application.
db = DuckDBConnection()
