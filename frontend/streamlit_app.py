import streamlit as st

from utils.state import init_state
from utils.auth import login, logout

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="FitTrack AI",
    page_icon="💪",
    layout="wide"
)

# ---------------------------------------------------------
# Initialize Session State
# ---------------------------------------------------------
init_state()

st.markdown(
    """
    <style>
        .main-title {
            text-align: center;
            font-size: 42px;
            font-weight: bold;
            color: #4F46E5;
        }

        .subtitle {
            text-align: center;
            color: #94A3B8;
            margin-bottom: 25px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------------------------
# Authentication
# ---------------------------------------------------------
if not st.session_state.logged_in:
    st.title("💪 FitTrack AI")

    st.write(
        "Sign in to access your fitness dashboard "
        "and workout assistant."
    )

    login()
    st.stop()

# ---------------------------------------------------------
# Sidebar
# ---------------------------------------------------------
# ---------------------------------------------------------
# Sidebar
# ---------------------------------------------------------

st.markdown("""
<style>

section[data-testid="stSidebar"] {
    background-color: #111827;
}

</style>
""", unsafe_allow_html=True)

st.sidebar.image(
    "https://img.icons8.com/fluency/96/dumbbell.png",
    width=75
)

st.sidebar.title("💪 FitTrack AI")

user = st.session_state.get("user", {})

st.sidebar.success(
    f"👋 Welcome\n{user.get('name', 'User')}"
)

st.sidebar.divider()

# ---------------------------------------------------------
# Quick Stats
# ---------------------------------------------------------
st.sidebar.subheader("Quick Stats")

st.sidebar.metric(
    "Weight Entries",
    len(st.session_state.get("weights", []))
)

st.sidebar.metric(
    "Workout Logs",
    len(st.session_state.get("workout_logs", []))
)

st.sidebar.divider()

# ---------------------------------------------------------
# Navigation Pages
# ---------------------------------------------------------
pg_home = st.Page(
    "pages/home.py",
    title="Home",
    icon="🏠"
)

pg_assistant = st.Page(
    "pages/workout_assistant.py",
    title="Workout Assistant",
    icon="🏋️"
)

pg_weights = st.Page(
    "pages/weight_tracking.py",
    title="Weight Tracking",
    icon="⚖️"
)

pg_settings = st.Page(
    "pages/settings.py",
    title="Settings",
    icon="⚙️"
)
pg_workouts = st.Page(
    "pages/workout_log.py",
    title="Workout Log",
    icon="🏃"
)

# ---------------------------------------------------------
# Navigation Groups
# ---------------------------------------------------------
navigation = st.navigation(
    {
        "Home": [pg_home],
        "Fitness Tools": [
            pg_assistant,
            pg_weights,
            pg_workouts,
        ],
        "Account": [pg_settings],
    }
)

st.sidebar.divider()

# ---------------------------------------------------------
# Logout
# ---------------------------------------------------------
if st.sidebar.button(
    "🚪 Logout",
    use_container_width=True
):
    logout()
    st.rerun()

# ---------------------------------------------------------
# Run Selected Page
# ---------------------------------------------------------
navigation.run()