from typing import Dict, Any

from uuid import uuid4
from fastapi.testclient import TestClient

from tests.conftest import gen_payload

def test_creation_without_optional_param(test_client: TestClient):
    res = test_client.post("/user/create", json=gen_payload())
    assert res.status_code == 200
    json = res.json()
    assert json['success']


def test_creation_with_optional_param(test_client: TestClient):
    req = {**gen_payload(), 'sendNotifications': False}
    res = test_client.post("user/create", json=req)
    assert res.status_code == 200
    json = res.json()
    assert json['success']


def test_creation_without_email_param(test_client: TestClient):
    no_email = gen_payload()
    no_email.pop('email')
    res = test_client.post("/user/create", json=no_email)
    assert res.status_code == 422


def test_creation_without_unique_email(test_client: TestClient, test_user: Dict[str, Any]):
    res = test_client.post("/user/create", json=test_user)
    assert res.status_code == 200
    json = res.json()
    assert not json['success']
    assert json['message'] == 'There is already a user with that email!'


# def test_creation_invalid_email():
#     pass


# def test_creation_invalid_phone():
    # pass    
