import streamlit as st
from utils.auth import logout


def init_state():
    """Initialize Streamlit session state variables."""

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if "username" not in st.session_state:
        st.session_state.username = None

    if "token" not in st.session_state:
        st.session_state.token = None

    if "user" not in st.session_state:
        st.session_state.user = {}

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if "weight_data" not in st.session_state:
        st.session_state.weight_data = []

    if "weights" not in st.session_state:
        st.session_state.weights = []

    if "workout_logs" not in st.session_state:
        st.session_state.workout_logs = []