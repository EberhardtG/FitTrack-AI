import os

import requests
import streamlit as st

BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://localhost:8000"
)

def send_query(text):
    headers = {}
    if "token" in st.session_state and st.session_state.token:
        headers["Authorization"] = f"Bearer {st.session_state.token}"

    try:
        response = requests.post(
            f"{BACKEND_URL}/workouts/ask",
            json={"question": text},  
            headers=headers,
            timeout=100
        )
        response.raise_for_status()
        return response.json()

    except Exception as e:
        return {
            "route": "error",
            "answer": "Backend unavailable.",
            "reason": str(e),
            "sources": None
        }



def get_weights():
    headers = {}
    if "token" in st.session_state and st.session_state.token:
        headers["Authorization"] = f"Bearer {st.session_state.token}"

    response = requests.get(f"{BACKEND_URL}/weights", headers=headers)
    response.raise_for_status()
    return response.json()


def add_weight(value):
    headers = {}
    if "token" in st.session_state and st.session_state.token:
        headers["Authorization"] = f"Bearer {st.session_state.token}"

    response = requests.post(
        f"{BACKEND_URL}/weights",
        json={"value": value},
        headers=headers
    )
    response.raise_for_status()
    return response.json()


def delete_weight(weight_id):
    headers = {}
    if "token" in st.session_state and st.session_state.token:
        headers["Authorization"] = f"Bearer {st.session_state.token}"

    response = requests.delete(
        f"{BACKEND_URL}/weights/{weight_id}",
        headers=headers
    )
    response.raise_for_status()
    return True

def get_workout_logs():

    headers = {}

    if (
        "token" in st.session_state
        and st.session_state.token
    ):
        headers["Authorization"] = (
            f"Bearer {st.session_state.token}"
        )

    response = requests.get(
        f"{BACKEND_URL}/workout_logs/",
        headers=headers
    )

    response.raise_for_status()

    return response.json()


def add_workout_log(
    workout_type,
    exercise_name,
    duration_minutes,
    calories_burned
):

    headers = {}

    if (
        "token" in st.session_state
        and st.session_state.token
    ):
        headers["Authorization"] = (
            f"Bearer {st.session_state.token}"
        )

    response = requests.post(
        f"{BACKEND_URL}/workout_logs/",
        json={
            "workout_type": workout_type,
            "exercise_name": exercise_name,
            "duration_minutes": duration_minutes,
            "calories_burned": calories_burned
        },
        headers=headers
    )

    response.raise_for_status()

    return response.json()


def delete_workout_log(log_id):

    headers = {}

    if (
        "token" in st.session_state
        and st.session_state.token
    ):
        headers["Authorization"] = (
            f"Bearer {st.session_state.token}"
        )

    response = requests.delete(
        f"{BACKEND_URL}/workout_logs/{log_id}",
        headers=headers
    )

    response.raise_for_status()

    return True

def reindex_documents():

    headers = {}

    if (
        "token" in st.session_state
        and st.session_state.token
    ):
        headers["Authorization"] = (
            f"Bearer {st.session_state.token}"
        )

    response = requests.post(
        f"{BACKEND_URL}/rag/reindex",
        headers=headers,
        timeout=300
    )

    response.raise_for_status()

    return response.json()

def get_me():
    headers = {}

    if "token" in st.session_state and st.session_state.token:
        headers["Authorization"] = (
            f"Bearer {st.session_state.token}"
        )

    response = requests.get(
        f"{BACKEND_URL}/auth/me",
        headers=headers
    )

    response.raise_for_status()

    return response.json()

