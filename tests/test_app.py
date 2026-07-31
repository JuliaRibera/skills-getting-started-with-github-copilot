from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_duplicate_signup_is_rejected():
    # Arrange
    activity_name = "Chess Club"
    email = "duplicate.student@mergington.edu"

    # Act
    first_response = client.post(
        f"/activities/{activity_name}/signup?email={email}",
    )
    second_response = client.post(
        f"/activities/{activity_name}/signup?email={email}",
    )

    # Assert
    assert first_response.status_code == 200
    assert second_response.status_code == 400
    assert "already signed up" in second_response.json()["detail"].lower()


def test_unregister_removes_participant():
    # Arrange
    activity_name = "Chess Club"
    email = "remove.me@mergington.edu"

    # Act
    signup_response = client.post(
        f"/activities/{activity_name}/signup?email={email}",
    )
    unregister_response = client.delete(
        f"/activities/{activity_name}/unregister?email={email}",
    )
    activities_response = client.get("/activities")

    # Assert
    assert signup_response.status_code == 200
    assert unregister_response.status_code == 200
    assert unregister_response.json()["message"].startswith("Removed")
    assert email not in activities_response.json()[activity_name]["participants"]
