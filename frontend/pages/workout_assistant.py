import streamlit as st

from utils.api_client import (
    send_query,
    get_weights
)


def render_workout_assistant():

    st.title("🏋️ Workout Assistant")
    st.caption(
    "🏋️ AI-powered fitness coaching based on your workout and weight history."
)

    # --------------------------------------------------
    # Chat History Initialization
    # --------------------------------------------------

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # --------------------------------------------------
    # Sidebar Chat Controls
    # --------------------------------------------------

    st.sidebar.subheader("Chat")

    if st.sidebar.button(
        "✨ New Conversation",
        use_container_width=True,
    ):
        st.session_state.chat_history = []
        st.rerun()

    st.sidebar.caption(
    f"{len(st.session_state.chat_history)//2} conversation turns"
)

    st.caption(
        "Ask questions about workouts, muscle gain, fat loss, recovery, and fitness progress."
    )

    # --------------------------------------------------
    # Authentication Check
    # --------------------------------------------------

    if not st.session_state.get("logged_in"):
        st.warning(
            "Please log in to use the Workout Assistant."
        )
        st.stop()

    # --------------------------------------------------
    # Weight Check
    # --------------------------------------------------

    try:

        weights = get_weights()

        if not weights:
            st.info(
                "💡 To receive personalized recommendations, log at least one weight entry first."
            )

    except Exception:

        st.warning(
            "Unable to verify weight history."
        )

    # --------------------------------------------------
    # Render Existing Messages
    # --------------------------------------------------

    for message in st.session_state.chat_history:

        with st.chat_message(
            message["role"]
        ):

            st.markdown(
                message["content"]
            )

            if (
                message["role"] == "assistant"
                and message.get("sources")
            ):

                with st.expander(
                    "📚 Sources"
                ):

                    for source in message["sources"]:
                        st.write(source)

    # --------------------------------------------------
    # Chat Input
    # --------------------------------------------------

    prompt = st.chat_input(
        "Ask about workouts, recovery, weight loss, muscle gain..."
    )

    if prompt:

        # ------------------------------
        # Verify Weight History
        # ------------------------------

        try:

            weights = get_weights()

            if not weights:

                with st.chat_message(
                    "assistant"
                ):
                    st.warning(
                        "Please log at least one weight entry before using the Workout Assistant."
                    )

                st.stop()

        except Exception:

            with st.chat_message(
                "assistant"
            ):
                st.error(
                    "Unable to verify weight history."
                )

            st.stop()

        # ------------------------------
        # Store User Message
        # ------------------------------

        st.session_state.chat_history.append(
            {
                "role": "user",
                "content": prompt,
            }
        )

        with st.chat_message(
            "user"
        ):
            st.markdown(prompt)

        # ------------------------------
        # Query Backend
        # ------------------------------

        try:

            with st.chat_message(
                "assistant"
            ):

                with st.spinner(
                    "Thinking..."
                ):

                    response = send_query(
                        prompt
                    )

                    recommendation = (
                        response.get(
                            "recommendation"
                        )
                        or "No recommendation available."
                    )

                    reasoning = (
                        response.get(
                            "reasoning"
                        )
                        or ""
                    )

                    assistant_message = (
                        f"{recommendation}\n\n"
                        f"### Reasoning\n\n"
                        f"{reasoning}"
                    )

                    st.markdown(
                        assistant_message
                    )

                    if response.get(
                        "sources"
                    ):

                        with st.expander(
                            "📚 Sources"
                        ):

                            for source in response[
                                "sources"
                            ]:
                                st.write(
                                    source
                                )

            st.session_state.chat_history.append(
                {
                    "role": "assistant",
                    "content": assistant_message,
                    "sources": response.get(
                        "sources",
                        [],
                    ),
                }
            )

        except Exception as e:

            error_message = (
                f"Unable to contact the Workout Assistant.\n\n{e}"
            )

            st.session_state.chat_history.append(
                {
                    "role": "assistant",
                    "content": error_message,
                }
            )

            with st.chat_message(
                "assistant"
            ):
                st.error(
                    error_message
                )


# --------------------------------------------------
# Streamlit Entrypoint
# --------------------------------------------------

render_workout_assistant()