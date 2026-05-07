"""Tests for DELETE /activities/{activity_name}/unregister endpoint"""

import pytest


def test_unregister_success(client, fresh_activities):
    """Test successful unregistration from an activity"""
    email = "test1@mergington.edu"

    # Verify participant is initially signed up
    response = client.get("/activities")
    initial_data = response.json()
    assert email in initial_data["Chess Club"]["participants"]

    # Unregister
    response = client.delete(
        "/activities/Chess%20Club/unregister",
        params={"email": email}
    )

    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]
    assert "Chess Club" in data["message"]


def test_unregister_removes_participant_from_activity(client, fresh_activities):
    """Test that unregister actually removes the participant"""
    email = "test1@mergington.edu"

    # Initially has 1 participant
    response = client.get("/activities")
    initial_data = response.json()
    assert len(initial_data["Chess Club"]["participants"]) == 1

    # Unregister
    client.delete("/activities/Chess%20Club/unregister", params={"email": email})

    # Check participant was removed
    response = client.get("/activities")
    updated_data = response.json()
    assert len(updated_data["Chess Club"]["participants"]) == 0
    assert email not in updated_data["Chess Club"]["participants"]


def test_unregister_nonexistent_email_fails(client, fresh_activities):
    """Test that unregistering non-existent email fails"""
    response = client.delete(
        "/activities/Gym%20Class/unregister",
        params={"email": "notsignedup@mergington.edu"}
    )

    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "not signed up" in data["detail"].lower()


def test_unregister_nonexistent_activity_fails(client, fresh_activities):
    """Test that unregistering from non-existent activity fails"""
    response = client.delete(
        "/activities/Nonexistent%20Activity/unregister",
        params={"email": "test@mergington.edu"}
    )

    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"].lower()


def test_unregister_activity_name_case_sensitive(client, fresh_activities):
    """Test that activity names are case sensitive for unregister"""
    email = "test1@mergington.edu"

    # Try unregistering with wrong case
    response = client.delete(
        "/activities/chess%20club/unregister",  # lowercase
        params={"email": email}
    )

    # Should fail because "chess club" != "Chess Club"
    assert response.status_code == 404


def test_unregister_twice_fails(client, fresh_activities):
    """Test that unregistering the same person twice fails"""
    email = "test1@mergington.edu"

    # First unregister should succeed
    response1 = client.delete("/activities/Chess%20Club/unregister", params={"email": email})
    assert response1.status_code == 200

    # Second unregister should fail
    response2 = client.delete("/activities/Chess%20Club/unregister", params={"email": email})
    assert response2.status_code == 400
    data = response2.json()
    assert "detail" in data
    assert "not signed up" in data["detail"].lower()


def test_unregister_empty_email_fails(client, fresh_activities):
    """Test that unregistering with empty email fails"""
    response = client.delete("/activities/Gym%20Class/unregister", params={"email": ""})

    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "cannot be empty" in data["detail"].lower()