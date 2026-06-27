"""Streamlit UI for the Customer Analytics Query Agent.

Launch with: streamlit run src/ui/app.py
"""

import streamlit as st
import pandas as pd
import altair as alt

from src.agent.query_engine import query_engine
from src.agent.sql_executor import executor, SQLValidationError
from src.agent.response_formatter import formatter


# -- Page config ------------------------------------------------------------
st.set_page_config(
    page_title="Customer Analytics Agent",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Customer Analytics - APE & Cust Growth Agent")
st.caption("Ask questions about APE and customer growth insights data in plain English.")

# -- Session state ----------------------------------------------------------
if "history" not in st.session_state:
    st.session_state.history = []


# -- Chart builders ---------------------------------------------------------

def build_bar_chart(data: pd.DataFrame) -> alt.Chart:
    """Build an Altair bar chart with value labels on each bar."""
    # Reset index to make the categorical column available
    df = data.reset_index()
    cat_col = df.columns[0]
    val_col = df.columns[1]

    # Determine if this is a percentage column
    is_pct = any(s in val_col.lower() for s in ("pct", "rate", "share"))

    bars = (
        alt.Chart(df)
        .mark_bar(color="#1f77b4", cornerRadiusTopLeft=3, cornerRadiusTopRight=3)
        .encode(
            x=alt.X(f"{cat_col}:N", title=None, sort=None),
            y=alt.Y(f"{val_col}:Q", title=None),
            tooltip=[f"{cat_col}:N", alt.Tooltip(f"{val_col}:Q", format=",.0f")],
        )
    )

    # Value labels on bars
    if is_pct:
        labels = (
            alt.Chart(df)
            .mark_text(dy=-10, fontSize=11, fontWeight="bold", color="#333")
            .encode(
                x=alt.X(f"{cat_col}:N", sort=None),
                y=alt.Y(f"{val_col}:Q"),
                text=alt.Text(f"{val_col}:Q", format=".1%"),
            )
        )
    else:
        labels = (
            alt.Chart(df)
            .mark_text(dy=-10, fontSize=11, fontWeight="bold", color="#333")
            .encode(
                x=alt.X(f"{cat_col}:N", sort=None),
                y=alt.Y(f"{val_col}:Q"),
                text=alt.Text(f"{val_col}:Q", format=",.0f"),
            )
        )

    return (bars + labels).properties(height=350)


def build_line_chart(data: pd.DataFrame) -> alt.Chart:
    """Build an Altair line chart with value labels on data points."""
    df = data.reset_index()
    cat_col = df.columns[0]
    val_col = df.columns[1]

    line = (
        alt.Chart(df)
        .mark_line(color="#1f77b4", point={"filled": True, "size": 60})
        .encode(
            x=alt.X(f"{cat_col}:N", title=None, sort=None),
            y=alt.Y(f"{val_col}:Q", title=None),
            tooltip=[f"{cat_col}:N", alt.Tooltip(f"{val_col}:Q", format=",.0f")],
        )
    )

    labels = (
        alt.Chart(df)
        .mark_text(dy=-15, fontSize=11, fontWeight="bold", color="#333")
        .encode(
            x=alt.X(f"{cat_col}:N", sort=None),
            y=alt.Y(f"{val_col}:Q"),
            text=alt.Text(f"{val_col}:Q", format=",.0f"),
        )
    )

    return (line + labels).properties(height=350)


# -- Input ------------------------------------------------------------------
with st.container():
    col1, col2 = st.columns([5, 1])
    with col1:
        question = st.text_input(
            "Your question",
            placeholder='e.g. "How many HNW customers does each LBU have?"',
            label_visibility="collapsed",
        )
    with col2:
        submit = st.button("Ask", type="primary", use_container_width=True)

# -- Process question -------------------------------------------------------
if submit and question.strip():
    with st.spinner("Analyzing your question..."):
        try:
            sql = query_engine.generate_sql(question)
        except Exception as e:
            st.error(f"LLM error: {e}")
            st.stop()

        try:
            result = executor.execute(sql)
        except SQLValidationError as e:
            st.error(f"SQL validation failed: {e}")
            with st.expander("🔍 Generated SQL (failed)", expanded=True):
                st.code(sql, language="sql")
            st.stop()

        response = formatter.format(question, sql, result)

        # Save to history
        st.session_state.history.append(response)

# -- Results ----------------------------------------------------------------
if st.session_state.history:
    latest = st.session_state.history[-1]

    st.divider()

    # -- Business summary --
    if latest.get("summary"):
        st.markdown(latest["summary"])

    # -- Chart --
    chart_type = latest.get("chart_type", "none")
    chart_data = latest.get("chart_data")

    if chart_type != "none" and chart_data is not None and not chart_data.empty:
        st.subheader("📈 Visual")
        if chart_type == "bar":
            chart = build_bar_chart(chart_data)
            st.altair_chart(chart, use_container_width=True)
        elif chart_type == "line":
            chart = build_line_chart(chart_data)
            st.altair_chart(chart, use_container_width=True)

    # -- Data table --
    st.subheader("📋 Data")
    st.dataframe(
        latest["table"],
        use_container_width=True,
        hide_index=True,
    )

    # -- SQL transparency --
    with st.expander("🔍 View generated SQL", expanded=False):
        st.code(latest["sql"], language="sql")

# -- Question history -------------------------------------------------------
if len(st.session_state.history) > 1:
    with st.expander(
        f"📋 Question history ({len(st.session_state.history)} queries)",
        expanded=False,
    ):
        for i, h in enumerate(reversed(st.session_state.history[:-1]), 1):
            st.markdown(
                f"**Q{len(st.session_state.history) - i}:** "
                f"{h['sql'][:120]}..."
            )
            st.caption(
                f"Rows: {h['row_count']}  •  "
                f"{h.get('summary', '')[:120]}..."
            )
            st.divider()

# -- Sidebar ----------------------------------------------------------------
with st.sidebar:
    st.header("About")
    st.markdown("""
    This agent answers business questions about life insurance
    customer analytics using a local LLM (Llama 3.1 8B via Ollama).

    **Data**: 57,600 aggregated rows across 10 markets,
    3 wealth segments, 6 life stages, and 5 product holding flags.

    **Model**: llama3.1:8b running locally.

    **How it works**:
    1. You ask a question in plain English
    2. The LLM converts it to SQL
    3. The SQL runs against DuckDB
    4. Results are summarized with business insights and charts
    """)

    st.divider()

    st.header("Sample Questions")
    st.markdown("""
    - How many customers do we have in total?
    - Show me customer count by wealth segment
    - How many HNW customers does each LBU have?
    - What percentage of customers hold medical insurance in PHKL?
    - Compare new vs existing premium in PACS
    - Which market has the highest total premium?
    - Break down customer count by market and tenure
    - What is the average premium per customer by tenure in PLUK?
    - Which market has the highest HNW customer share?
    - Compare HNW vs Mass average premium in each market
    - How is PHKL performing?
    - Show me the top 5 markets by HNW customer proportion
    """)
