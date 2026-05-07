"""Tests for POST /activities/{activity_name}/signup endpoint"""

import pytest


def test_signup_success(client, fresh_activities, test_email):
    """Test successful signup to an activity"""
    response = client.post(
        "/activities/Gym%20Class/signup",
        params={"email": test_email}
    )

    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert test_email in data["message"]
    assert "Gym Class" in data["message"]


def test_signup_adds_participant_to_activity(client, fresh_activities, test_email):
    """Test that signup actually adds the participant to the activity"""
    # Initially empty
    response = client.get("/activities")
    initial_data = response.json()
    assert len(initial_data["Gym Class"]["participants"]) == 0

    # Sign up
    client.post("/activities/Gym%20Class/signup", params={"email": test_email})

    # Check participant was added
    response = client.get("/activities")
    updated_data = response.json()
    assert len(updated_data["Gym Class"]["participants"]) == 1
    assert test_email in updated_data["Gym Class"]["participants"]


def test_signup_duplicate_email_fails(client, fresh_activities):
    """Test that signing up twice with same email fails"""
    email = "duplicate@mergington.edu"

    # First signup should succeed
    response1 = client.post("/activities/Gym%20Class/signup", params={"email": email})
    assert response1.status_code == 200

    # Second signup should fail
    response2 = client.post("/activities/Gym%20Class/signup", params={"email": email})
    assert response2.status_code == 400
    data = response2.json()
    assert "detail" in data
    assert "already signed up" in data["detail"].lower()


def test_signup_nonexistent_activity_fails(client, fresh_activities, test_email):
    """Test that signing up for non-existent activity fails"""
    response = client.post(
        "/activities/Nonexistent%20Activity/signup",
        params={"email": test_email}
    )

    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"].lower()


def test_signup_activity_name_case_sensitive(client, fresh_activities, test_email):
    """Test that activity names are case sensitive"""
    # Try signing up with wrong case
    response = client.post(
        "/activities/gym%20class/signup",  # lowercase
        params={"email": test_email}
    )

    # Should fail because "gym class" != "Gym Class"
    assert response.status_code == 404


def test_signup_empty_email_fails(client, fresh_activities):
    """Test that empty email fails"""
    response = client.post("/activities/Gym%20Class/signup", params={"email": ""})

    # Should fail with 400 Bad Request
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "cannot be empty" in data["detail"].lower()


def test_signup_multiple_different_emails_succeeds(client, fresh_activities):
    """Test that multiple different emails can sign up for same activity"""
    emails = ["student1@mergington.edu", "student2@mergington.edu", "student3@mergington.edu"]

    # All should succeed
    for email in emails:
        response = client.post("/activities/Gym%20Class/signup", params={"email": email})
        assert response.status_code == 200

    # Check all were added
    response = client.get("/activities")
    data = response.json()
    assert len(data["Gym Class"]["participants"]) == 3
    assert set(data["Gym Class"]["participants"]) == set(emails)