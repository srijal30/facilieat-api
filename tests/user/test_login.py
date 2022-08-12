from typing import Any, Dict
from fastapi.testclient import TestClient

def test_successful_login(test_client: TestClient, test_user: Dict[str, Any]):
    # test the login
    login_payload = \
        {
            'email': test_user['email'],
            'password': test_user['password']
        }
    login_res = test_client.post('user/login', json=login_payload)
    assert login_res.status_code == 200
    json = login_res.json()
    assert json['success']
    assert json['data']['token']
    

def test_unsuccesful_login_user_not_found(test_client: TestClient):
    login_payload = \
        {
            'email': 'nevermadeanemaillikethis@something.com',  # this email should not exist in db
            'password': 'randompassword'  # password doesnt matter
        }
    res = test_client.post('user/login', json=login_payload)
    assert res.status_code == 200
    json = res.json()
    assert not json['success']
    assert json['message'] == 'No user with that email!'  


def test_unsuccessful_login_incorrect_info(test_client: TestClient, test_user: Dict[str, Any]):
    login_payload = \
        {
            'email': test_user['email'],  # correct
            'password': test_user['password'] + 'wrong'  # wrong
        }
    res = test_client.post('user/login', json=login_payload)
    assert res.status_code == 200
    json = res.json()
    assert not json['success']
    assert json['message'] == 'Invalid email or password!'
