import streamlit as st

def render_home():
    st.markdown(
    '<p class="main-title">💪 FitTrack AI</p>',
    unsafe_allow_html=True
)

    st.markdown(
    '<p class="subtitle">AI-Powered Fitness Tracking & Workout Recommendations</p>',
    unsafe_allow_html=True
)

    user = st.session_state.get("user", {})
    name = user.get("name", "Athlete")

    st.title(f"💪 Welcome back, {name}!")

    st.markdown("""
    Your personal AI-powered fitness assistant is ready to help you stay on track.

    ### What would you like to do today?

    🏋️ **Workout Assistant**
    - Ask workout questions
    - Get personalized recommendations
    - Receive guidance based on your workout history

    ⚖️ **Weight Tracking**
    - Log new weight entries
    - Visualize progress over time
    - Identify trends and milestones

    ⚙️ **Settings**
    - Manage account preferences
    - Clear chat history
    - Control application options
    """)

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.info(
            """
            🏋️ **Need training advice?**

            Visit Workout Assistant for AI-generated
            recommendations based on your logged activity.
            """
        )

    with col2:
        st.info(
            """
            ⚖️ **Tracking progress?**

            Visit Weight Tracking to log weigh-ins
            and monitor long-term trends.
            """
        )

    st.divider()

    st.subheader("Today's Focus")

    st.success(
        "Consistency beats intensity. Small improvements made "
        "regularly produce long-term fitness results."
    )

render_home()