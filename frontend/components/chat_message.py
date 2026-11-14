import streamlit as st


def render_chat_message(role: str, content: str):
    """
    Render a chat message in a consistent format.
    """

    if role == "user":
        st.markdown(
            f"""
            <div style="
                padding:10px;
                border-radius:10px;
                background-color:#E8F0FE;
                margin-bottom:10px;
            ">
                <strong>🧑 You</strong><br>
                {content}
            </div>
            """,
            unsafe_allow_html=True
        )

    else:
        st.markdown(
            f"""
            <div style="
                padding:10px;
                border-radius:10px;
                background-color:#F5F5F5;
                margin-bottom:10px;
            ">
                <strong>🤖 Assistant</strong><br>
                {content}
            </div>
            """,
            unsafe_allow_html=True
        )