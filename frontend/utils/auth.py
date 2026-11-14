import streamlit as st
import requests

import os

BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://localhost:8000"
)


def login():
    st.subheader("Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        try:
            # Authenticate
            response = requests.post(
                f"{BACKEND_URL}/auth/token",
                json={
                    "email": email,
                    "password": password
                },
                timeout=10
            )

            response.raise_for_status()

            data = response.json()

            # Store JWT
            st.session_state.token = data["access_token"]

            # Mark as authenticated
            st.session_state.logged_in = True

            # Fetch user profile
            user_res = requests.get(
                f"{BACKEND_URL}/auth/me",
                headers={
                    "Authorization": f"Bearer {st.session_state.token}"
                },
                timeout=10
            )

            user_res.raise_for_status()

            st.session_state.user = user_res.json()

            # Store username separately for convenience
            st.session_state.username = (
                st.session_state.user.get("name")
            )

            st.rerun()

        except requests.exceptions.HTTPError:
            st.error("Invalid email or password.")

        except requests.exceptions.ConnectionError:
            st.error(
                "Unable to reach the backend API."
            )

        except Exception as e:
            st.error(f"Unexpected Error: {e}")


def logout():

    st.session_state.logged_in = False
    st.session_state.token = None
    st.session_state.user = {}
    st.session_state.username = None
    st.session_state.chat_history = []
