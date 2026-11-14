import pytest

def auth_headers(client):
    """Helper to register + login and return auth headers."""
    client.post("/auth/register", json={
        "email": "logs@example.com",
        "password": "password123",
        "name": "Tester"
    })

    token_res = client.post("/auth/token", json={
        "email": "logs@example.com",
        "password": "password123"
    })

    token = token_res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


# -----------------------------
# CREATE WORKOUT LOG
# -----------------------------

def test_create_workout_log_success(client):
    headers = auth_headers(client)

    res = client.post("/workout_logs", json={
        "exercise_name": "Bench Press",
        "duration_minutes": 45
    }, headers=headers)

    assert res.status_code == 201
    data = res.json()
    assert data["exercise_name"] == "Bench Press"
    assert data["duration_minutes"] == 45
    assert "id" in data


# -----------------------------
# GET WORKOUT LOGS
# -----------------------------

def test_get_workout_logs(client):
    headers = auth_headers(client)

    # Create two logs
    client.post("/workout_logs", json={
        "exercise_name": "Squats",
        "duration_minutes": 30
    }, headers=headers)

    client.post("/workout_logs", json={
        "exercise_name": "Deadlift",
        "duration_minutes": 40
    }, headers=headers)

    res = client.get("/workout_logs", headers=headers)
    assert res.status_code == 200

    data = res.json()
    assert len(data) == 2
    assert data[0]["exercise_name"] in ["Squats", "Deadlift"]


# -----------------------------
# UPDATE WORKOUT LOG
# -----------------------------

def test_update_workout_log_success(client):
    headers = auth_headers(client)

    # Create log
    res = client.post("/workout_logs", json={
        "exercise_name": "Running",
        "duration_minutes": 20
    }, headers=headers)
    log_id = res.json()["id"]

    # Update log
    res2 = client.patch(f"/workout_logs/{log_id}", json={
        "exercise_name": "Jogging",
        "duration_minutes": 25
    }, headers=headers)

    assert res2.status_code == 200
    data = res2.json()
    assert data["exercise_name"] == "Jogging"
    assert data["duration_minutes"] == 25


def test_update_workout_log_not_found(client):
    headers = auth_headers(client)

    res = client.patch("/workout_logs/999", json={
        "exercise_name": "New Name"
    }, headers=headers)

    assert res.status_code == 404
    assert res.json()["detail"] == "Workout log entry not found"


def test_update_workout_log_no_fields(client):
    headers = auth_headers(client)

    # Create log
    res = client.post("/workout_logs", json={
        "exercise_name": "Pushups",
        "duration_minutes": 10
    }, headers=headers)
    log_id = res.json()["id"]

    # Missing fields
    res2 = client.patch(f"/workout_logs/{log_id}", json={}, headers=headers)
    assert res2.status_code == 400
    assert res2.json()["detail"] == "No fields provided for update"


def test_update_workout_log_unrealistic_duration(client):
    headers = auth_headers(client)

    # Create log
    res = client.post("/workout_logs", json={
        "exercise_name": "Cycling",
        "duration_minutes": 30
    }, headers=headers)
    log_id = res.json()["id"]

    # Unrealistic duration
    res2 = client.patch(f"/workout_logs/{log_id}", json={
        "duration_minutes": 2000
    }, headers=headers)

    assert res2.status_code == 400
    assert res2.json()["detail"] == "Duration value unrealistic"


# -----------------------------
# DELETE WORKOUT LOG
# -----------------------------

def test_delete_workout_log_success(client):
    headers = auth_headers(client)

    # Create log
    res = client.post("/workout_logs", json={
        "exercise_name": "Yoga",
        "duration_minutes": 60
    }, headers=headers)
    log_id = res.json()["id"]

    # Delete
    res2 = client.delete(f"/workout_logs/{log_id}", headers=headers)
    assert res2.status_code == 204


def test_delete_workout_log_not_found(client):
    headers = auth_headers(client)

    res = client.delete("/workout_logs/999", headers=headers)
    assert res.status_code == 404
    assert res.json()["detail"] == "Workout log entry not found"
