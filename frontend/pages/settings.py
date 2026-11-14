import streamlit as st
from utils.auth import logout
from utils.api_client import (
    get_me,
    reindex_documents
)

def render_settings():
    st.title("⚙️ Settings")

    if not st.session_state.get("logged_in"):
        st.warning("Please log in to access settings.")
        st.stop()

    try:
        user = get_me()
    except Exception:
        st.error("Unable to load user profile.")
        st.stop()

    profile_tab, app_tab = st.tabs(
        ["Profile", "App Preferences"]
    )

    # ----------------------------------
    # Profile Tab
    # ----------------------------------
    with profile_tab:
        st.subheader("Account Information")

        st.write(f"**Email:** {user.get('email')}")
        st.write(f"**User ID:** {user.get('id')}")

        st.divider()

        if st.button("Log Out"):
            logout()
            st.success("Logged out successfully.")
            st.rerun()

    # ----------------------------------
    # App Preferences Tab
    # ----------------------------------
    with app_tab:

        st.subheader("Chat Settings")

    if st.button("Clear Workout Assistant History"):
        st.session_state.chat_history = []
        st.success(
            "Workout Assistant history cleared."
        )
        st.rerun()

    st.divider()

    st.subheader("Future Preferences")

    st.radio(
        "Preferred Units",
        ["Pounds (lbs)", "Kilograms (kg)"],
        horizontal=True,
        disabled=True
    )

    st.toggle(
        "Enable AI Insights",
        value=True,
        disabled=True
    )

    with st.expander("Danger Zone"):
        st.warning(
            "Account deletion has not been implemented."
        )

    st.divider()

    st.subheader("Knowledge Base")

    if st.button(
        "🔄 Re-Index Documents"
    ):

        try:

            with st.spinner(
                "Rebuilding vector database..."
            ):

                reindex_documents()

            st.success(
                "Knowledge base successfully re-indexed."
            )

        except Exception as e:

            st.error(
                f"Re-index failed: {e}"
            )
    # --------------------------------------------------
# Streamlit Entrypoint
# --------------------------------------------------

render_settings()

        