"""Response Formatter -- formats query results for the Streamlit UI.

Generates a plain-English summary with business insights, formats numbers
with thousands separators and percentages with 1 decimal place, and
recommends chart types for visual display.
"""

import pandas as pd


class ResponseFormatter:
    """Formats SQL query results into a user-friendly, business-oriented response."""

    def format(
        self, question: str, sql: str, result: pd.DataFrame,
    ) -> dict:
        """Build a structured response from query results.

        Returns a dict with:
        - summary: plain-English business summary of the results
        - table: the result DataFrame (formatted for display)
        - sql: the generated SQL (for transparency)
        - chart_type: recommended chart (bar, line, or none)
        - chart_data: DataFrame prepared for chart rendering
        - row_count: number of rows returned
        """
        row_count = len(result)
        chart_type = self.recommend_chart(result)
        chart_data = self._prepare_chart_data(result, chart_type)

        summary = self._build_summary(question, result, row_count)

        return {
            "summary": summary,
            "table": result,
            "sql": sql,
            "chart_type": chart_type,
            "chart_data": chart_data,
            "row_count": row_count,
        }

    # ------------------------------------------------------------------
    # Number formatting
    # ------------------------------------------------------------------

    @staticmethod
    def format_number(value: float) -> str:
        """Format a number with thousands separators.

        Examples: 1234567 -> "1,234,567", 1234.5 -> "1,234.5"
        """
        if pd.isna(value):
            return "-"
        if abs(value) >= 1_000_000_000:
            return f"{value/1_000_000_000:,.1f}B"
        if abs(value) >= 1_000_000:
            return f"{value/1_000_000:,.1f}M"
        if abs(value) >= 1_000:
            return f"{value:,.0f}"
        if value == int(value):
            return f"{int(value):,}"
        return f"{value:,.2f}"

    @staticmethod
    def format_pct(value: float) -> str:
        """Format a proportion as percentage with 1 decimal place.

        Examples: 0.1234 -> "12.3%", 0.05 -> "5.0%"
        """
        if pd.isna(value):
            return "-"
        return f"{value * 100:.1f}%"

    # ------------------------------------------------------------------
    # Chart recommendation
    # ------------------------------------------------------------------

    @staticmethod
    def recommend_chart(result: pd.DataFrame) -> str:
        """Determine the best chart type based on result structure.

        Heuristics:
        - Single row -> "none"
        - 2+ rows with 1 categorical col + 1+ numeric cols -> "bar"
        - Tenure/time-like categorical col -> "line"
        - LLM hint overrides if it makes structural sense
        """
        if len(result) <= 1:
            return "none"

        numeric_cols = [
            c for c in result.columns
            if result[c].dtype in ("int64", "float64", "Int64", "Float64")
        ]
        categorical_cols = [
            c for c in result.columns
            if result[c].dtype not in ("int64", "float64", "Int64", "Float64")
        ]

        # Need at least 1 categorical + 1 numeric for a chart
        if not categorical_cols or not numeric_cols:
            return "none"

        # Tenure or ordered sequence -> line
        tenure_cols = [c for c in categorical_cols if "tenure" in c.lower()]
        if tenure_cols and len(result) > 2:
            return "line"

        # Default: bar for comparisons
        if categorical_cols and numeric_cols:
            return "bar"

        return "none"

    @staticmethod
    def _prepare_chart_data(
        result: pd.DataFrame, chart_type: str,
    ) -> pd.DataFrame | None:
        """Prepare a DataFrame suitable for Streamlit chart rendering.

        Sets the first categorical column as index, keeps numeric columns.
        """
        if chart_type == "none" or len(result) <= 1:
            return None

        categorical_cols = [
            c for c in result.columns
            if result[c].dtype not in ("int64", "float64", "Int64", "Float64")
        ]
        numeric_cols = [
            c for c in result.columns
            if result[c].dtype in ("int64", "float64", "Int64", "Float64")
        ]

        if not categorical_cols or not numeric_cols:
            return None

        df = result.copy()
        # Use first categorical col as index
        index_col = categorical_cols[0]
        df = df.set_index(index_col)
        # Keep only numeric columns for chart
        df = df[numeric_cols]
        return df

    # ------------------------------------------------------------------
    # Summary builder (business analyst voice)
    # ------------------------------------------------------------------

    def _build_summary(
        self, question: str, result: pd.DataFrame, row_count: int,
    ) -> str:
        """Generate a plain-English business summary."""
        parts: list[str] = []

        if row_count == 0:
            return f"No data found for: {question}"

        # Identify key columns
        numeric_cols = [
            c for c in result.columns
            if result[c].dtype in ("int64", "float64", "Int64", "Float64")
        ]
        categorical_cols = [
            c for c in result.columns
            if result[c].dtype not in ("int64", "float64", "Int64", "Float64")
        ]

        # Single-row answer
        if row_count == 1:
            return self._single_row_summary(result, numeric_cols, categorical_cols)

        # Multi-row: identify top/bottom, trends, notable patterns
        parts.append(self._multi_row_insights(result, numeric_cols, categorical_cols))

        return "  ".join(parts)

    def _single_row_summary(
        self, result: pd.DataFrame, numeric_cols: list[str],
        categorical_cols: list[str],
    ) -> str:
        """Summarize a single-row result."""
        parts = []
        for col in numeric_cols:
            val = result[col].iloc[0]
            col_display = col.replace("_", " ")
            if any(s in col.lower() for s in ("pct", "rate", "share")):
                parts.append(f"{col_display}: **{self.format_pct(val)}**")
            elif "premium" in col.lower():
                parts.append(f"{col_display}: **{self.format_number(val)}**")
            elif "customer" in col.lower() or "count" in col.lower():
                parts.append(f"{col_display}: **{self.format_number(val)}**")
            else:
                parts.append(f"{col_display}: {self.format_number(val)}")
        return "  ".join(parts) if parts else f"Returned 1 row."

    def _multi_row_insights(
        self, result: pd.DataFrame, numeric_cols: list[str],
        categorical_cols: list[str],
    ) -> str:
        """Generate insight bullets for multi-row results."""
        parts = []
        if not numeric_cols or not categorical_cols:
            return f"Returned {row_count} rows."

        row_count = len(result)

        # Find the primary numeric column (prefer premium, then customer_count)
        primary_num = None
        for pref in ("total_premium", "annual_premium", "total_customers",
                      "customer_count", "avg_premium"):
            if pref in numeric_cols:
                primary_num = pref
                break
        if primary_num is None:
            primary_num = numeric_cols[0]

        # Find top and bottom
        cat_col = categorical_cols[0]
        top_row = result.loc[result[primary_num].idxmax()]
        bottom_row = result.loc[result[primary_num].idxmin()]

        # Format the primary metric
        top_val = top_row[primary_num]
        bottom_val = bottom_row[primary_num]
        is_pct = any(s in primary_num.lower() for s in ("pct", "rate", "share"))

        fmt = self.format_pct if is_pct else self.format_number

        # Top performer
        top_label = str(top_row[cat_col])
        parts.append(
            f"**{top_label}** leads with {fmt(top_val)}"
            + (f" {primary_num.replace('_', ' ')}" if not is_pct else "")
        )

        # Gap insight: if 3+ rows, show the spread
        if row_count >= 3:
            if is_pct:
                spread = top_val - bottom_val
                parts.append(
                    f"-- a {self.format_pct(spread)} gap vs **{bottom_row[cat_col]}** ({self.format_pct(bottom_val)})"
                )
            else:
                ratio = top_val / bottom_val if bottom_val > 0 else 0
                if ratio >= 2:
                    parts.append(
                        f"-- {ratio:.1f}x vs **{bottom_row[cat_col]}** ({fmt(bottom_val)})"
                    )
                else:
                    parts.append(
                        f"-- vs **{bottom_row[cat_col]}** at {fmt(bottom_val)}"
                    )

        # Secondary insight: customer/premium relationship if both present
        has_customers = any("customer" in c.lower() and "count" not in c.lower()
                           for c in numeric_cols)
        has_premium = any("premium" in c.lower() for c in numeric_cols)
        if has_customers and has_premium and row_count >= 2:
            cust_col = next(c for c in numeric_cols if "customer" in c.lower())
            prem_col = next(c for c in numeric_cols if "premium" in c.lower())
            # Find the row with highest avg premium (if not already an avg col)
            if "avg" not in prem_col.lower():
                result_copy = result.copy()
                result_copy["_avg"] = result_copy[prem_col] / result_copy[cust_col]
                highest_avg_row = result_copy.loc[result_copy["_avg"].idxmax()]
                parts.append(
                    f"Highest avg premium/customer: "
                    f"**{highest_avg_row[cat_col]}** "
                    f"({self.format_number(highest_avg_row[prem_col] / highest_avg_row[cust_col])})"
                )

        return "  ".join(parts)


# Singleton instance
formatter = ResponseFormatter()
