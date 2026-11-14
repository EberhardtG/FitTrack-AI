import pytest


def auth_headers(client):
    """Helper to register + login and return auth headers."""
    client.post("/auth/register", json={
        "email": "test@example.com",
        "password": "password123",
        "name": "Tester"
    })

    token_res = client.post("/auth/token", json={
        "email": "test@example.com",
        "password": "password123"
    })

    token = token_res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_create_weight_success(client):
    headers = auth_headers(client)

    res = client.post("/weights", json={"value": 180}, headers=headers)
    assert res.status_code == 201

    data = res.json()
    assert data["value"] == 180
    assert "id" in data


def test_create_weight_invalid_value(client):
    headers = auth_headers(client)

    res = client.post(
        "/weights",
        json={"value": -5},
        headers=headers
    )

    assert res.status_code == 422


def test_create_weight_unrealistic_value(client):
    headers = auth_headers(client)

    res = client.post(
        "/weights",
        json={"value": 2000},
        headers=headers
    )

    assert res.status_code == 422


def test_create_weight_twice_same_day(client):
    headers = auth_headers(client)

    # First weight
    client.post("/weights", json={"value": 180}, headers=headers)

    # Second weight same day
    res = client.post("/weights", json={"value": 181}, headers=headers)
    assert res.status_code == 400
    assert res.json()["detail"] == "Weight already logged today"


def test_get_weights(client):
    headers = auth_headers(client)

    # Create two weights on different days
    client.post("/weights", json={"value": 180}, headers=headers)

    res = client.get("/weights", headers=headers)
    assert res.status_code == 200

    data = res.json()
    assert len(data) == 1
    assert data[0]["value"] == 180


def test_update_weight_success(client):
    headers = auth_headers(client)

    # Create weight
    res = client.post("/weights", json={"value": 180}, headers=headers)
    weight_id = res.json()["id"]

    # Update weight
    res2 = client.patch(f"/weights/{weight_id}", json={"value": 185}, headers=headers)
    assert res2.status_code == 200

    data = res2.json()
    assert data["value"] == 185


def test_update_weight_not_found(client):
    headers = auth_headers(client)

    res = client.patch("/weights/999", json={"value": 185}, headers=headers)
    assert res.status_code == 404
    assert res.json()["detail"] == "Weight entry not found"


def test_update_weight_no_fields(client):
    headers = auth_headers(client)

    # Create weight
    res = client.post("/weights", json={"value": 180}, headers=headers)
    weight_id = res.json()["id"]

    # Missing fields
    res2 = client.patch(f"/weights/{weight_id}", json={}, headers=headers)
    assert res2.status_code == 400
    assert res2.json()["detail"] == "No fields provided for update"


def test_delete_weight_success(client):
    headers = auth_headers(client)

    # Create weight
    res = client.post("/weights", json={"value": 180}, headers=headers)
    weight_id = res.json()["id"]

    # Delete
    res2 = client.delete(f"/weights/{weight_id}", headers=headers)
    assert res2.status_code == 204


def test_delete_weight_not_found(client):
    headers = auth_headers(client)

    res = client.delete("/weights/999", headers=headers)
    assert res.status_code == 404
    assert res.json()["detail"] == "Weight entry not found"
