import pytest

sample_cryptid = {
    "name": "Bigfoot",
    "description": "Large, hairy creature in North America.",
    "image_url": "http://example.com/bigfoot.jpg",
}

updated_cryptid = {
    "name": "Updated Bigfoot",
    "description": "A mysterious creature updated.",
    "image_url": "http://example.com/bigfoot_updated.jpg",
}


@pytest.fixture
def create_sample_cryptid(client):
    response = client.post("/cryptids/", json=sample_cryptid)
    assert response.status_code == 201
    return response.json()


# --- Create ---


def test_create_cryptid(client):
    response = client.post("/cryptids/", json=sample_cryptid)
    assert response.status_code == 201
    body = response.json()
    assert isinstance(body["id"], int)
    assert {k: body[k] for k in sample_cryptid} == sample_cryptid


@pytest.mark.parametrize("missing_field", sample_cryptid.keys())
def test_create_cryptid_missing_field(client, missing_field):
    payload = {k: v for k, v in sample_cryptid.items() if k != missing_field}
    response = client.post("/cryptids/", json=payload)
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", missing_field]


# --- Read ---


def test_list_cryptids(client):
    for i in range(3):
        client.post("/cryptids/", json={**sample_cryptid, "name": f"Bigfoot {i}"})

    response = client.get("/cryptids/")
    assert response.status_code == 200
    assert len(response.json()) == 3


@pytest.mark.parametrize(
    "params, expected_count",
    [
        ({"limit": 2}, 2),
        ({"skip": 2}, 1),
        ({"skip": 5}, 0),
    ],
    ids=["limit", "skip", "skip-past-end"],
)
def test_list_cryptids_pagination(client, params, expected_count):
    for i in range(3):
        client.post("/cryptids/", json={**sample_cryptid, "name": f"Bigfoot {i}"})

    response = client.get("/cryptids/", params=params)
    assert response.status_code == 200
    assert len(response.json()) == expected_count


def test_get_cryptid(client, create_sample_cryptid):
    cryptid_id = create_sample_cryptid["id"]
    response = client.get(f"/cryptids/{cryptid_id}")
    assert response.status_code == 200
    assert response.json() == create_sample_cryptid


# --- Update ---


def test_update_cryptid(client, create_sample_cryptid):
    cryptid_id = create_sample_cryptid["id"]
    response = client.put(f"/cryptids/{cryptid_id}", json=updated_cryptid)
    assert response.status_code == 200
    assert response.json() == {"id": cryptid_id, **updated_cryptid}

    # Confirm the change was actually saved, not just echoed back
    response = client.get(f"/cryptids/{cryptid_id}")
    assert response.json() == {"id": cryptid_id, **updated_cryptid}


@pytest.mark.parametrize("missing_field", updated_cryptid.keys())
def test_update_cryptid_missing_field(client, create_sample_cryptid, missing_field):
    cryptid_id = create_sample_cryptid["id"]
    payload = {k: v for k, v in updated_cryptid.items() if k != missing_field}
    response = client.put(f"/cryptids/{cryptid_id}", json=payload)
    assert response.status_code == 422

    # The original record should be untouched
    response = client.get(f"/cryptids/{cryptid_id}")
    assert response.json() == create_sample_cryptid


# --- Delete ---


def test_delete_cryptid(client, create_sample_cryptid):
    cryptid_id = create_sample_cryptid["id"]
    response = client.delete(f"/cryptids/{cryptid_id}")
    assert response.status_code == 204
    response = client.get(f"/cryptids/{cryptid_id}")
    assert response.status_code == 404


# --- Errors shared across endpoints ---


@pytest.mark.parametrize(
    "method, kwargs",
    [
        ("get", {}),
        ("put", {"json": sample_cryptid}),
        ("delete", {}),
    ],
    ids=["get", "put", "delete"],
)
def test_cryptid_not_found(client, method, kwargs):
    response = client.request(method, "/cryptids/9999", **kwargs)
    assert response.status_code == 404
    assert response.json() == {"detail": "Cryptid not found"}


@pytest.mark.parametrize(
    "method, kwargs",
    [
        ("get", {}),
        ("put", {"json": sample_cryptid}),
        ("delete", {}),
    ],
    ids=["get", "put", "delete"],
)
def test_cryptid_invalid_id(client, method, kwargs):
    response = client.request(method, "/cryptids/abc", **kwargs)
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["path", "cryptid_id"]
