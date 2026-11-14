import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker

from app.db import Base, get_db
from app.main import app

def test_register_user(client):
    payload = {
        "email": "test@example.com",
        "password": "password123",
        "name": "Test User"
    }

    response = client.post("/auth/register", json=payload)
    assert response.status_code == 201

    data = response.json()
    assert data["email"] == payload["email"].lower()
    assert data["name"] == payload["name"]
    assert "id" in data


def test_register_duplicate_email(client):
    payload = {
        "email": "duplicate@example.com",
        "password": "password123",
        "name": "User One"
    }

    # First registration
    client.post("/auth/register", json=payload)

    # Second registration should fail
    response = client.post("/auth/register", json=payload)
    assert response.status_code == 400
    assert response.json()["detail"] == "User with this email already exists"


def test_login_success(client):
    # Register first
    client.post("/auth/register", json={
        "email": "login@example.com",
        "password": "password123",
        "name": "Login User"
    })

    # Login
    response = client.post("/auth/token", json={
        "email": "login@example.com",
        "password": "password123"
    })

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_password(client):
    client.post("/auth/register", json={
        "email": "wrongpass@example.com",
        "password": "correctpass",
        "name": "Wrong Pass"
    })

    response = client.post("/auth/token", json={
        "email": "wrongpass@example.com",
        "password": "incorrectpass"
    })

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"
