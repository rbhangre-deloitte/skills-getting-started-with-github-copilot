"""Tests for the Mergington High School Activities API.

Uses AAA (Arrange-Act-Assert) pattern to structure each test clearly.
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    """Provide a test client for the FastAPI app."""
    return TestClient(app)


class TestGetActivities:
    """Tests for GET /activities endpoint."""

    def test_get_activities_returns_all_activities(self, client):
        """Test that GET /activities returns all activities with status 200."""
        # Arrange
        # (client fixture is already arranged)

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert len(data) > 0
        assert "Chess Club" in data
        assert "Programming Class" in data

    def test_get_activities_has_required_fields(self, client):
        """Test that each activity has required fields."""
        # Arrange
        # (client fixture is already arranged)

        # Act
        response = client.get("/activities")

        # Assert
        data = response.json()
        for activity_name, details in data.items():
            assert "description" in details
            assert "schedule" in details
            assert "max_participants" in details
            assert "participants" in details
            assert isinstance(details["participants"], list)


class TestSignupForActivity:
    """Tests for POST /activities/{activity_name}/signup endpoint."""

    def test_signup_new_participant_succeeds(self, client):
        """Test signing up a new participant for an activity."""
        # Arrange
        activity_name = "Chess Club"
        email = "newstudent@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert activity_name in data["message"]

    def test_signup_duplicate_participant_rejected(self, client):
        """Test that signing up an already registered participant fails."""
        # Arrange
        activity_name = "Programming Class"
        email = "emma@mergington.edu"  # Already signed up

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "already signed up" in data["detail"].lower()

    def test_signup_nonexistent_activity_not_found(self, client):
        """Test that signing up for a nonexistent activity returns 404."""
        # Arrange
        activity_name = "Nonexistent Club"
        email = "student@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "not found" in data["detail"].lower()


class TestRemoveParticipant:
    """Tests for DELETE /activities/{activity_name}/signup endpoint."""

    def test_remove_existing_participant_succeeds(self, client):
        """Test removing an existing participant from an activity."""
        # Arrange
        activity_name = "Gym Class"
        email = "john@mergington.edu"  # Already signed up

        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert "Unregistered" in data["message"]

    def test_remove_nonexistent_participant_not_found(self, client):
        """Test that removing a nonexistent participant returns 404."""
        # Arrange
        activity_name = "Soccer Team"
        email = "notregistered@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "not found" in data["detail"].lower()

    def test_remove_from_nonexistent_activity_not_found(self, client):
        """Test that removing from a nonexistent activity returns 404."""
        # Arrange
        activity_name = "Nonexistent Club"
        email = "student@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "not found" in data["detail"].lower()
