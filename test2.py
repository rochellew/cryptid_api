import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app, get_db
from app.database import Base  # Import your Base for model creation
from app.models import Cryptid  # Import your model

# In-memory SQLite database URL
TEST_DATABASE_URL = "sqlite:///:memory:"

# Create an in-memory engine for testing
test_engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

# Fixture to set up and tear down the database with in-memory engine
@pytest.fixture(scope="function")
def override_get_db():
    # Create tables in the in-memory database
    Base.metadata.create_all(bind=test_engine)
    
    # Override the `get_db` dependency to use the in-memory test engine
    def get_test_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = get_test_db
    yield  # Test runs here
    app.dependency_overrides.clear()  # Clean up dependency override
    Base.metadata.drop_all(bind=test_engine)

# TestClient setup
client = TestClient(app)

# Sample data for testing
sample_cryptid = {
    "name": "Bigfoot",
    "description": "Large, hairy creature in North America.",
    "image_url": "http://example.com/bigfoot.jpg"
}

@pytest.fixture
def create_sample_cryptid(override_get_db):
    # Creates a cryptid entry for testing purposes
    response = client.post("/cryptids/", json=sample_cryptid)
    assert response.status_code == 201
    return response.json()

def test_create_cryptid(override_get_db):
    response = client.post("/cryptids/", json=sample_cryptid)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == sample_cryptid["name"]
    assert data["description"] == sample_cryptid["description"]

def test_get_cryptid(override_get_db, create_sample_cryptid):
    cryptid_id = create_sample_cryptid["id"]
    response = client.get(f"/cryptids/{cryptid_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == sample_cryptid["name"]
    assert data["description"] == sample_cryptid["description"]

def test_update_cryptid(override_get_db, create_sample_cryptid):
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

def test_delete_cryptid(override_get_db, create_sample_cryptid):
    cryptid_id = create_sample_cryptid["id"]
    response = client.delete(f"/cryptids/{cryptid_id}")
    assert response.status_code == 204
    # Verify deletion
    response = client.get(f"/cryptids/{cryptid_id}")
    assert response.status_code == 404
