"""Integration and edge case tests across multiple endpoints"""

import pytest


def test_signup_updates_participant_count(client, fresh_activities, test_email):
    """Test that signup increases participant count"""
    # Get initial count
    response = client.get("/activities")
    initial_data = response.json()
    initial_count = len(initial_data["Gym Class"]["participants"])

    # Sign up
    client.post("/activities/Gym%20Class/signup", params={"email": test_email})

    # Check count increased
    response = client.get("/activities")
    updated_data = response.json()
    updated_count = len(updated_data["Gym Class"]["participants"])

    assert updated_count == initial_count + 1


def test_unregister_updates_participant_count(client, fresh_activities):
    """Test that unregister decreases participant count"""
    email = "test1@mergington.edu"

    # Get initial count
    response = client.get("/activities")
    initial_data = response.json()
    initial_count = len(initial_data["Chess Club"]["participants"])

    # Unregister
    client.delete("/activities/Chess%20Club/unregister", params={"email": email})

    # Check count decreased
    response = client.get("/activities")
    updated_data = response.json()
    updated_count = len(updated_data["Chess Club"]["participants"])

    assert updated_count == initial_count - 1


def test_multiple_signups_same_activity(client, fresh_activities):
    """Test that multiple different students can sign up for same activity"""
    emails = ["alice@mergington.edu", "bob@mergington.edu", "charlie@mergington.edu"]

    # All sign up for Gym Class
    for email in emails:
        response = client.post("/activities/Gym%20Class/signup", params={"email": email})
        assert response.status_code == 200

    # Verify all are registered
    response = client.get("/activities")
    data = response.json()
    participants = data["Gym Class"]["participants"]

    assert len(participants) == 3
    assert set(participants) == set(emails)


def test_signup_then_unregister_round_trip(client, fresh_activities, test_email):
    """Test complete signup -> unregister cycle"""
    # Sign up
    response = client.post("/activities/Gym%20Class/signup", params={"email": test_email})
    assert response.status_code == 200

    # Verify signed up
    response = client.get("/activities")
    data = response.json()
    assert test_email in data["Gym Class"]["participants"]

    # Unregister
    response = client.delete("/activities/Gym%20Class/unregister", params={"email": test_email})
    assert response.status_code == 200

    # Verify unregistered
    response = client.get("/activities")
    data = response.json()
    assert test_email not in data["Gym Class"]["participants"]


def test_activities_isolation_between_tests(client, fresh_activities):
    """Test that activities are properly isolated between tests"""
    # This test should always start with fresh data
    response = client.get("/activities")
    data = response.json()

    # Verify test fixture data is consistent
    assert len(data["Chess Club"]["participants"]) == 1
    assert len(data["Programming Class"]["participants"]) == 2
    assert len(data["Gym Class"]["participants"]) == 0

    # Make a change
    client.post("/activities/Gym%20Class/signup", params={"email": "newstudent@mergington.edu"})

    # Verify change was made
    response = client.get("/activities")
    data = response.json()
    assert len(data["Gym Class"]["participants"]) == 1

    # This change should not persist to other tests due to fixture isolation


def test_activity_capacity_not_exceeded_by_signup(client, fresh_activities):
    """Test that signup doesn't prevent exceeding capacity (no validation yet)"""
    # Gym Class has max_participants = 30
    # Sign up 31 students (should succeed since no validation)
    for i in range(31):
        email = f"student{i}@mergington.edu"
        response = client.post("/activities/Gym%20Class/signup", params={"email": email})
        assert response.status_code == 200

    # Verify all were added
    response = client.get("/activities")
    data = response.json()
    assert len(data["Gym Class"]["participants"]) == 31


def test_special_characters_in_email(client, fresh_activities):
    """Test emails with special characters work"""
    special_emails = [
        "test+tag@mergington.edu",
        "test.dot@mergington.edu",
        "test-dash@mergington.edu"
    ]

    for email in special_emails:
        response = client.post("/activities/Gym%20Class/signup", params={"email": email})
        assert response.status_code == 200

    # Verify all were added
    response = client.get("/activities")
    data = response.json()
    participants = data["Gym Class"]["participants"]
    assert len(participants) == 3
    assert set(participants) == set(special_emails)