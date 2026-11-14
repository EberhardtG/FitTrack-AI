import streamlit as st
import pandas as pd

from components.weight_graph import render_weight_graph

from utils.api_client import (
    get_weights,
    add_weight,
    delete_weight
)


def render_weight_tracking():

    st.title("⚖️ Weight Tracking")

    # --------------------------------------------------
    # Authentication Check
    # --------------------------------------------------

    if not st.session_state.get("logged_in"):
        st.warning("Please log in to track your weight.")
        st.stop()

    # --------------------------------------------------
    # Load Weight Data
    # --------------------------------------------------

    try:
        weights = get_weights()

        

    except Exception:
        st.error("Unable to load weight data.")
        st.stop()

    # --------------------------------------------------
    # Build DataFrame
    # --------------------------------------------------

    df = None

    if weights:

        df = pd.DataFrame(weights)

        if "created_at" in df.columns:
            df["created_at"] = pd.to_datetime(
                df["created_at"]
            )

            df = df.sort_values("created_at")

    # --------------------------------------------------
    # Tabs
    # --------------------------------------------------

    log_tab, trends_tab, manage_tab = st.tabs(
        [
            "📝 Weight Log",
            "📈 Progress Trends",
            "⚙️ Manage Entries"
        ]
    )

    # ==================================================
    # TAB 1 - WEIGHT LOG
    # ==================================================

    with log_tab:

        st.subheader("Add New Weight")

        new_weight = st.number_input(
            "Weight (lbs)",
            min_value=1.0,
            max_value=1000.0,
            step=0.1
        )

        if st.button("Add Weight"):

            try:
                add_weight(new_weight)

                st.success(
                    "Weight added successfully."
                )

                st.rerun()

            except Exception:
                st.error(
                    "Failed to add weight."
                )

        st.divider()

        st.subheader("Weight History")

        if not weights:

            st.info(
                "No weight entries yet."
            )

        else:

            st.dataframe(
                df[["created_at", "value"]]
                .sort_values(
                    "created_at",
                    ascending=False
                ),
                use_container_width=True
            )

    # ==================================================
    # TAB 2 - PROGRESS TRENDS
    # ==================================================

    with trends_tab:

        st.subheader("Progress Overview")

        if not weights:

            st.info(
                "Add weight entries to begin viewing progress trends."
            )

        else:

            latest_weight = df.iloc[-1]["value"]
            starting_weight = df.iloc[0]["value"]

            total_change = (
                latest_weight
                - starting_weight
            )

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Current Weight",
                    f"{latest_weight:.1f} lbs"
                )

            with col2:
                st.metric(
                    "Starting Weight",
                    f"{starting_weight:.1f} lbs"
                )

            with col3:
                st.metric(
                    "Overall Change",
                    f"{total_change:.1f} lbs"
                )

            st.divider()

            st.subheader("Weight Trend")

            render_weight_graph(df)

            st.divider()

            st.subheader(
                "Summary Statistics"
            )

            stat_col1, stat_col2, stat_col3 = st.columns(3)

            with stat_col1:
                st.metric(
                    "Highest",
                    f"{df['value'].max():.1f} lbs"
                )

            with stat_col2:
                st.metric(
                    "Lowest",
                    f"{df['value'].min():.1f} lbs"
                )

            with stat_col3:
                st.metric(
                    "Average",
                    f"{df['value'].mean():.1f} lbs"
                )

    # ==================================================
    # TAB 3 - MANAGE ENTRIES
    # ==================================================

    with manage_tab:

        st.subheader(
            "Delete Weight Entries"
        )

        if not weights:

            st.info(
                "No weight entries available."
            )

        else:

            delete_id = st.selectbox(
                "Select an entry",
                options=[w["id"] for w in weights],
                format_func=lambda wid:
                    (
                        f"{wid} - "
                        f"{next(w['value'] for w in weights if w['id'] == wid)} lbs"
                    )
            )

            if st.button(
                "Delete Selected Entry",
                type="secondary"
            ):

                try:
                    delete_weight(delete_id)

                    st.success(
                        "Weight entry deleted successfully."
                    )

                    st.rerun()

                except Exception:
                    st.error(
                        "Failed to delete weight entry."
                    )


# --------------------------------------------------
# Streamlit Entrypoint
# --------------------------------------------------

render_weight_tracking()