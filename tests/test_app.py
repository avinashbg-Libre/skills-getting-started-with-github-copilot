from fastapi.testclient import TestClient
from urllib.parse import quote
import pytest

from src.app import app, activities

client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert "Chess Club" in data
    assert isinstance(data["Chess Club"]["participants"], list)


def test_signup_and_unregister_flow():
    activity = "Chess Club"
    test_email = "testuser+pytest@example.com"

    # Ensure clean starting state for this email
    if test_email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(test_email)

    # Sign up the test email
    resp = client.post(f"/activities/{quote(activity)}/signup", params={"email": test_email})
    assert resp.status_code == 200
    assert test_email in activities[activity]["participants"]

    # Verify via GET
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert test_email in data[activity]["participants"]

    # Unregister the test email
    resp = client.delete(f"/activities/{quote(activity)}/participants", params={"email": test_email})
    assert resp.status_code == 200
    assert test_email not in activities[activity]["participants"]

    # Verify removed via GET
    resp = client.get("/activities")
    data = resp.json()
    assert test_email not in data[activity]["participants"]
