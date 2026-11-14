import streamlit as st


def render_sources_block(sources):
    """
    Display recommendation sources in a consistent format.
    """

    if not sources:
        return

    with st.expander("📚 Sources Used"):

        for source in sources:
            st.write(f"• {source}")