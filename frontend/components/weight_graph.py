import streamlit as st
import pandas as pd


def render_weight_graph(df: pd.DataFrame):
    """
    Render a weight trend chart.

    Parameters:
        df (pd.DataFrame):
            Expected columns:
            - created_at
            - value
    """

    if df.empty:
        st.info("No weight data available.")
        return

    st.line_chart(
        df.sort_values("created_at"),
        x="created_at",
        y="value",
        use_container_width=True,
    )
