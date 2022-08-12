from typing import Any, Dict
from fastapi.testclient import TestClient

keys = [
    'email',
    'phone',
    'firstName',
    'lastName',
    'status',
    'sendNotifications'
]

def test_user_access_with_auth(test_client: TestClient, test_token: str):
    res = test_client.post("/user/user", json={'token': test_token})
    assert res.status_code == 200
    json = res.json()
    assert json['success']
    data = json['data']
    assert all(key in data for key in keys)


def test_user_access_without_auth(test_client: TestClient):
    res = test_client.post("/user/user", json={})
    assert res.status_code == 200
    json = res.json()
    assert not json['success']
    assert json['message'] == 'You are currently not logged in!'