import pytest
from fastapi.testclient import TestClient
from app.main import app  # Import your FastAPI app here

client = TestClient(app)

# Sample data for testing
sample_cryptid = {
    "name": "Bigfoot",
    "description": "Large, hairy creature in North America.",
    "image_url": "http://example.com/bigfoot.jpg"
}

@pytest.fixture
def create_sample_cryptid():
    # Creates a cryptid entry for testing purposes
    response = client.post("/cryptids/", json=sample_cryptid)
    assert response.status_code == 201
    return response.json()

def test_create_cryptid():
    response = client.post("/cryptids/", json=sample_cryptid)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == sample_cryptid["name"]
    assert data["description"] == sample_cryptid["description"]

def test_get_cryptid(create_sample_cryptid):
    print (create_sample_cryptid)
    cryptid_id = create_sample_cryptid["id"]
    response = client.get(f"/cryptids/{cryptid_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == sample_cryptid["name"]
    assert data["description"] == sample_cryptid["description"]

def test_update_cryptid(create_sample_cryptid):
    cryptid_id = create_sample_cryptid["id"]
    updated_data = {
        "name": "Updated Bigfoot",
        "description": "A mysterious creature updated.",
        "image_url": "http://example.com/bigfoot_updated.jpg"
    }
    response = client.put(f"/cryptids/{cryptid_id}", json=updated_data)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == updated_data["name"]
    assert data["description"] == updated_data["description"]

def test_delete_cryptid(create_sample_cryptid):
    cryptid_id = create_sample_cryptid["id"]
    response = client.delete(f"/cryptids/{cryptid_id}")
    assert response.status_code == 204
    # Verify deletion
    response = client.get(f"/cryptids/{cryptid_id}")
    assert response.status_code == 404
