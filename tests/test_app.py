import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

# Test: List activities

def test_list_activities():
    # Arrange
    # (No setup needed, uses in-memory DB)
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

# Test: Successful signup

def test_signup_for_activity():
    # Arrange
    activity = list(client.get("/activities").json().keys())[0]
    email = "testuser@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 200
    assert email in client.get(f"/activities").json()[activity]["participants"]

# Test: Prevent duplicate signup

def test_prevent_duplicate_signup():
    # Arrange
    activity = list(client.get("/activities").json().keys())[0]
    email = "dupeuser@mergington.edu"
    client.post(f"/activities/{activity}/signup?email={email}")
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]

# Test: Unregister participant

def test_unregister_participant():
    # Arrange
    activity = list(client.get("/activities").json().keys())[0]
    email = "removeuser@mergington.edu"
    client.post(f"/activities/{activity}/signup?email={email}")
    # Act
    response = client.delete(f"/activities/{activity}/unregister?email={email}")
    # Assert
    assert response.status_code == 200
    assert email not in client.get(f"/activities").json()[activity]["participants"]

# Test: Invalid activity

def test_invalid_activity():
    # Arrange
    invalid_activity = "nonexistent"
    email = "invalid@mergington.edu"
    # Act
    response = client.post(f"/activities/{invalid_activity}/signup?email={email}")
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]

# Test: Unregister non-existent participant

def test_unregister_nonexistent_participant():
    # Arrange
    activity = list(client.get("/activities").json().keys())[0]
    email = "ghost@mergington.edu"
    # Act
    response = client.delete(f"/activities/{activity}/unregister?email={email}")
    # Assert
    assert response.status_code == 404
    assert "Participant not found" in response.json()["detail"]
