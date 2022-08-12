from fastapi.testclient import TestClient

keys = [
    'email',
    'phone',
    'firstName',
    'lastName',
    'sendNotifications'
]

def test_user_access_with_auth(test_client: TestClient, test_token: str):
    res = test_client.post("/user/user", json={'token': test_token})
    assert res.status_code == 200
    json = res.json()
    print(json)
    assert json['success']
    data = json['data']
    assert all(key in data for key in keys)


def test_user_access_with_incorrect_auth(test_client: TestClient):
    res = test_client.post("/user/user", json={'token': 'obviouslywrong'})
    assert res.status_code == 200
    json = res.json()
    assert not json['success']
    assert json['message'] == 'Authentication details invalid!'
