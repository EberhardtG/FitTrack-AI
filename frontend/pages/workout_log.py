import streamlit as st
import pandas as pd

from utils.api_client import (
    get_workout_logs,
    add_workout_log,
    delete_workout_log
)


def render_workout_log():

    st.title("🏃 Workout Log")

    # --------------------------------------------------
    # Authentication Check
    # --------------------------------------------------

    if not st.session_state.get("logged_in"):
        st.warning(
            "Please log in to track workouts."
        )
        st.stop()

    # --------------------------------------------------
    # Load Workout Data
    # --------------------------------------------------

    try:

        workouts = get_workout_logs()

        # Keep sidebar metrics current
        st.session_state.workout_logs = workouts

    except Exception:

        st.error(
            "Unable to load workout logs."
        )

        st.stop()

    # --------------------------------------------------
    # Build DataFrame
    # --------------------------------------------------

    df = None

    if workouts:

        df = pd.DataFrame(workouts)

        if "created_at" in df.columns:

            df["created_at"] = pd.to_datetime(
                df["created_at"]
            )

            df = df.sort_values(
                "created_at"
            )

    # --------------------------------------------------
    # Tabs
    # --------------------------------------------------

    log_tab, history_tab, manage_tab = st.tabs(
        [
            "📝 Log Workout",
            "📊 Workout History",
            "⚙️ Manage Entries"
        ]
    )

    # ==================================================
    # TAB 1 - LOG WORKOUT
    # ==================================================

    with log_tab:

        st.subheader(
            "Add Workout"
        )

        workout_type = st.selectbox(
            "Workout Type",
            [
                "Strength",
                "Cardio",
                "Sports",
                "Mobility",
                "Recovery"
            ]
        )

        exercise_name = st.text_input(
            "Exercise Name"
        )

        duration_minutes = st.number_input(
            "Duration (minutes)",
            min_value=1,
            max_value=300,
            value=30
        )

        calories_burned = st.number_input(
            "Calories Burned",
            min_value=0,
            value=100
        )

        if st.button(
            "Add Workout"
        ):

            if not exercise_name.strip():

                st.error(
                    "Exercise name is required."
                )

            else:

                try:

                    add_workout_log(
                        workout_type,
                        exercise_name,
                        duration_minutes,
                        calories_burned
                    )

                    # Refresh sidebar workout count
                    st.session_state.workout_logs = (
                        get_workout_logs()
                    )

                    st.success(
                        "Workout logged successfully."
                    )

                    st.rerun()

                except Exception as e:

                    st.error(
                        f"Failed to add workout: {e}"
                    )

    # ==================================================
    # TAB 2 - HISTORY
    # ==================================================

    with history_tab:

        st.subheader(
            "Workout History"
        )

        if not workouts:

            st.info(
                "No workout entries yet."
            )

        else:

            st.dataframe(
                df[
                    [
                        "exercise_name",
                        "workout_type",
                        "duration_minutes",
                        "calories_burned",
                        "created_at"
                    ]
                ].sort_values(
                    "created_at",
                    ascending=False
                ),
                use_container_width=True
            )

            st.divider()

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(
                    "Total Workouts",
                    len(df)
                )

            with col2:

                st.metric(
                    "Total Minutes",
                    int(
                        df[
                            "duration_minutes"
                        ].sum()
                    )
                )

            with col3:

                st.metric(
                    "Calories Burned",
                    int(
                        df[
                            "calories_burned"
                        ].sum()
                    )
                )

    # ==================================================
    # TAB 3 - MANAGE
    # ==================================================

    with manage_tab:

        st.subheader(
            "Delete Workout Entries"
        )

        if not workouts:

            st.info(
                "No workout entries available."
            )

        else:

            delete_id = st.selectbox(
                "Select workout",
                options=[
                    w["id"]
                    for w in workouts
                ],
                format_func=lambda wid:
                    next(
                        (
                            f"{w['exercise_name']} "
                            f"({w['duration_minutes']} min)"
                        )
                        for w in workouts
                        if w["id"] == wid
                    )
            )

            if st.button(
                "Delete Workout",
                type="secondary"
            ):

                try:

                    delete_workout_log(
                        delete_id
                    )

                    # Refresh sidebar workout count
                    st.session_state.workout_logs = (
                        get_workout_logs()
                    )

                    st.success(
                        "Workout deleted successfully."
                    )

                    st.rerun()

                except Exception as e:

                    st.error(
                        f"Failed to delete workout: {e}"
                    )


# --------------------------------------------------
# Streamlit Entrypoint
# --------------------------------------------------

render_workout_log()