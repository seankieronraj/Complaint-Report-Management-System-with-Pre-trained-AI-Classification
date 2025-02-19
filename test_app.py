import pytest
from app import app

@pytest.fixture
# Creates a test client for the Flask app
def client():
    app.config["TESTING"] = True
    return app.test_client()

# Test creating a new complaint
def test_create_complaint(client):
    response = client.post("/complaints", json={
        "title": "Slow Internet",
        "description": "The internet connection is too slow."
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data["complaint"]["title"] == "Slow Internet"
    assert data["complaint"]["category"] in ["Billing", "Service", "Other"]


# Test retrieving all complaints
def test_get_complaints(client):
    client.post("/complaints", json={"title": "Test", "description": "Test complaint"})
    response = client.get("/complaints")
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)

# Test retrieving a complaint by ID
def test_get_specific_complaint(client):
    post_resp = client.post("/complaints", json={"title": "Specific", "description": "Find me"})
    complaint_id = post_resp.get_json()["complaint"]["id"]

    get_resp = client.get(f"/complaints/{complaint_id}")
    assert get_resp.status_code == 200
    assert get_resp.get_json()["id"] == complaint_id
    

# Test updating a complaint's title and description
def test_update_complaint(client):
    post_resp = client.post("/complaints", json={"title": "Old", "description": "Old desc"})
    complaint_id = post_resp.get_json()["complaint"]["id"]

    update_resp = client.put(f"/complaints/{complaint_id}", json={"title": "New Title", "description": "New desc"})
    updated_data = update_resp.get_json()["complaint"]
    assert updated_data["title"] == "New Title"
    assert update_resp.status_code == 200
    

# Test deleting a complaint.
def test_delete_complaint(client):
    post_resp = client.post("/complaints", json={"title": "Delete Me", "description": "Remove this"})
    complaint_id = post_resp.get_json()["complaint"]["id"]

    delete_resp = client.delete(f"/complaints/{complaint_id}")
    assert delete_resp.status_code == 200

    # Verify complaint no longer exists
    get_resp = client.get(f"/complaints/{complaint_id}")
    assert get_resp.status_code == 404
