from app.database import get_db
import pytest

sample_cryptid = {
    "name": "Bigfoot",
    "description": "Large, hairy creature in North America.",
    "image_url": "http://example.com/bigfoot.jpg"
}

@pytest.fixture
def create_sample_cryptid(client):
    response = client.post("/cryptids/", json=sample_cryptid)
    assert response.status_code == 201
    return response.json()

def test_create_cryptid(client):
    response = client.post("/cryptids/", json=sample_cryptid)
    assert response.status_code == 201

def test_get_cryptid(client, create_sample_cryptid):
    cryptid_id = create_sample_cryptid["id"]
    response = client.get(f"/cryptids/{cryptid_id}")
    assert response.status_code == 200

def test_update_cryptid(client, create_sample_cryptid):
    cryptid_id = create_sample_cryptid["id"]
    updated_data = {
        "name": "Updated Bigfoot",
        "description": "A mysterious creature updated.",
        "image_url": "http://example.com/bigfoot_updated.jpg"
    }
    response = client.put(f"/cryptids/{cryptid_id}", json=updated_data)
    assert response.status_code == 200

def test_delete_cryptid(client, create_sample_cryptid):
    cryptid_id = create_sample_cryptid["id"]
    response = client.delete(f"/cryptids/{cryptid_id}")
    assert response.status_code == 204
    response = client.get(f"/cryptids/{cryptid_id}")
    assert response.status_code == 404