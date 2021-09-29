import json

from fastapi import status


def test_create_product(client, normal_user_token_headers):
    data = {
        "nom": "SDE super",
        "cathegorie": "doogle",
        "description": "www.doogle.com",
    }
    response = client.post(
        "/jobs/create-product/", data=json.dumps(data), headers=normal_user_token_headers
    )
    assert response.status_code == 200
    assert response.json()["company"] == "doogle"
    assert response.json()["description"] == "python"


def test_read_product(client, normal_user_token_headers):
    data = {
        "nom": "SDE super",
        "cathegorie": "doogle",
        "description": "www.doogle.com",
    }
    response = client.post(
        "/jobs/create-product/", json.dumps(data), headers=normal_user_token_headers
    )

    response = client.get("/jobs/get/1/")
    assert response.status_code == 200
    assert response.json()["nom"] == "SDE super"


def test_read_products(client, normal_user_token_headers):
    data = {
        "nom": "SDE super",
        "cathegorie": "doogle",
        "description": "www.doogle.com",
    }
    client.post(
        "/jobs/create-product/", json.dumps(data), headers=normal_user_token_headers
    )
    client.post(
        "/jobs/create-product/", json.dumps(data), headers=normal_user_token_headers
    )

    response = client.get("/jobs/all/")
    assert response.status_code == 200
    assert response.json()[0]
    assert response.json()[1]


def test_update_a_products(client, normal_user_token_headers):
    data = {
        "nom": "New Job super",
        "cathegorie": "doogle",
        "description": "www.doogle.com",
    }
    client.post(
        "/jobs/create-product/", json.dumps(data), headers=normal_user_token_headers
    )
    data["title"] = "test new title"
    response = client.put("/jobs/update/1", json.dumps(data))
    assert response.json()["msg"] == "Successfully updated data."


def test_delete_a_product(client, normal_user_token_headers):
    data = {
        "nom": "New Job super",
        "cathegorie": "doogle",
        "description": "www.doogle.com",
    }
    client.post(
        "/jobs/create-product/", json.dumps(data), headers=normal_user_token_headers
    )
    client.delete("/jobs/delete/1", headers=normal_user_token_headers)
    response = client.get("/jobs/get/1/")
    assert response.status_code == status.HTTP_404_NOT_FOUND
