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
    assert json['success']
    data = json['data']
    assert all(key in data for key in keys)


def test_user_access_with_incorrect_auth(test_client: TestClient):
    res = test_client.post("/user/user", json={'token': 'obviouslywrong'})
    assert res.status_code == 200
    json = res.json()
    assert not json['success']
    assert json['message'] == 'Authentication details invalid!'


def test_change_user_info(test_client: TestClient, test_token: str):
    new_first_name = "Walter"
    new_last_name = "White"
    new_send_notifications = False
    change_payload = \
        {
            'token': test_token,
            'firstName': new_first_name,
            'lastName': new_last_name,
            'sendNotifications': new_send_notifications
        }
    change_res = test_client.post("/user/change", json=change_payload)
    assert change_res.status_code == 200
    assert change_res.json()['success']
    assert change_res.json()['message'] == 'Successfully changed user information!'
    # check that it actually changed
    test_changes_res = test_client.post("/user/user", json={'token': test_token})
    assert test_changes_res.status_code == 200
    assert test_changes_res.json()['success']
    changed_data = test_changes_res.json()['data']
    assert new_first_name == changed_data['firstName']
    assert new_last_name == changed_data['lastName']
    assert new_send_notifications == changed_data['sendNotifications']