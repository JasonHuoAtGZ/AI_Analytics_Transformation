"""Response Formatter — formats query results for the Streamlit UI.

Generates a plain-English summary and structures the output for display.
"""

import pandas as pd


class ResponseFormatter:
    """Formats SQL query results into a user-friendly response."""

    def format(
        self, question: str, sql: str, result: pd.DataFrame
    ) -> dict:
        """Build a structured response from query results.

        Returns a dict with:
        - summary: plain-English summary of the results
        - table: the result DataFrame
        - sql: the generated SQL (for transparency)
        - row_count: number of rows returned
        """
        row_count = len(result)

        summary = self._build_summary(question, result, row_count)

        return {
            "summary": summary,
            "table": result,
            "sql": sql,
            "row_count": row_count,
        }

    def _build_summary(
        self, question: str, result: pd.DataFrame, row_count: int
    ) -> str:
        """Generate a plain-English summary of the query results."""
        parts: list[str] = []

        # How many rows returned
        if row_count == 0:
            return f"No data found for: {question}"

        if row_count == 1:
            parts.append(f"Returned 1 row.")
        else:
            parts.append(f"Returned {row_count:,} rows.")

        # If the result has customer_count and/or annual_premium, summarize totals
        if "total_customers" in result.columns:
            tc = result["total_customers"].sum()
            parts.append(f"Total customers: {tc:,.0f}")
        elif "customer_count" in result.columns:
            tc = result["customer_count"].sum()
            parts.append(f"Total customers: {tc:,.0f}")

        if "total_premium" in result.columns:
            tp = result["total_premium"].sum()
            parts.append(self._fmt_premium(tp))
        elif "annual_premium" in result.columns:
            tp = result["annual_premium"].sum()
            parts.append(self._fmt_premium(tp))

        if "avg_premium" in result.columns:
            avg = result["avg_premium"].mean()
            parts.append(f"Average premium per customer: {avg:,.0f}")

        # If single column like hnw_pct or medical_holding_rate, format as %
        pct_cols = [c for c in result.columns if c.endswith("_pct") or c.endswith("_rate")]
        for col in pct_cols:
            if row_count == 1:
                parts.append(f"{col}: {result[col].iloc[0]:.1%}")
            else:
                parts.append(f"{col} range: {result[col].min():.1%} – {result[col].max():.1%}")

        # Top and bottom rows for ranked results
        if row_count > 1 and "market" in result.columns and "total_premium" in result.columns:
            top = result.iloc[0]
            bottom = result.iloc[-1]
            parts.append(
                f"Highest: {top['market']} ({self._fmt_premium(top['total_premium'])})"
            )
            if row_count > 2:
                parts.append(
                    f"Lowest: {bottom['market']} ({self._fmt_premium(bottom['total_premium'])})"
                )

        return " ".join(parts)

    @staticmethod
    def _fmt_premium(value: float) -> str:
        """Format premium value in human-readable form."""
        if abs(value) >= 1_000_000_000:
            return f"Total premium: {value/1_000_000_000:,.1f}B"
        elif abs(value) >= 1_000_000:
            return f"Total premium: {value/1_000_000:,.1f}M"
        elif abs(value) >= 1_000:
            return f"Total premium: {value/1_000:,.0f}K"
        else:
            return f"Total premium: {value:,.0f}"


# Singleton instance
formatter = ResponseFormatter()
