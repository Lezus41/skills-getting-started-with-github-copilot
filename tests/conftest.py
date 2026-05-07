import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    """FastAPI test client fixture"""
    return TestClient(app)


@pytest.fixture
def fresh_activities():
    """Reset activities to known test state before each test"""
    from src.app import activities

    # Store original activities to restore later
    original_activities = activities.copy()

    # Reset to test data
    activities.clear()
    activities.update({
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["test1@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["test2@mergington.edu", "test3@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": []
        }
    })

    yield activities

    # Restore original activities after test
    activities.clear()
    activities.update(original_activities)


@pytest.fixture
def test_email():
    """Common test email for signup tests"""
    return "student@mergington.edu"