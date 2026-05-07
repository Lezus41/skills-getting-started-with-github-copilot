"""Tests for GET /activities endpoint"""

import pytest


def test_get_activities_returns_all_activities(client, fresh_activities):
    """Test that GET /activities returns all activities"""
    response = client.get("/activities")

    assert response.status_code == 200
    data = response.json()

    # Should return all 3 test activities
    assert len(data) == 3
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert "Gym Class" in data


def test_get_activities_structure(client, fresh_activities):
    """Test that activities have the correct structure"""
    response = client.get("/activities")
    data = response.json()

    # Check Chess Club structure
    chess_club = data["Chess Club"]
    assert "description" in chess_club
    assert "schedule" in chess_club
    assert "max_participants" in chess_club
    assert "participants" in chess_club

    assert isinstance(chess_club["participants"], list)
    assert isinstance(chess_club["max_participants"], int)
    assert isinstance(chess_club["description"], str)
    assert isinstance(chess_club["schedule"], str)


def test_get_activities_participant_counts(client, fresh_activities):
    """Test that participant counts are correct"""
    response = client.get("/activities")
    data = response.json()

    # Chess Club should have 1 participant
    assert len(data["Chess Club"]["participants"]) == 1
    assert data["Chess Club"]["participants"] == ["test1@mergington.edu"]

    # Programming Class should have 2 participants
    assert len(data["Programming Class"]["participants"]) == 2
    assert data["Programming Class"]["participants"] == ["test2@mergington.edu", "test3@mergington.edu"]

    # Gym Class should have 0 participants
    assert len(data["Gym Class"]["participants"]) == 0
    assert data["Gym Class"]["participants"] == []


def test_get_activities_max_participants(client, fresh_activities):
    """Test that max_participants values are correct"""
    response = client.get("/activities")
    data = response.json()

    assert data["Chess Club"]["max_participants"] == 12
    assert data["Programming Class"]["max_participants"] == 20
    assert data["Gym Class"]["max_participants"] == 30