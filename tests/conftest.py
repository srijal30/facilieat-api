import os
from typing import Any, Dict
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from src.app import app


@pytest.fixture(scope='session', autouse=True)
def database_management():
    """Clears database"""
    os.system("rm data.sqlite")
    os.system("prisma db push")
    yield


@pytest.fixture()
def test_client() -> TestClient:
    """Activates TestClient context"""
    with TestClient(app) as client:
        yield client


@pytest.fixture()
def test_user(test_client: TestClient) -> Dict[str, Any]:
    """Creates and returns a test user"""
    create_payload = gen_payload()
    test_client.post("user/create", json=create_payload)
    yield create_payload


@pytest.fixture()
def test_token(test_client: TestClient, test_user: Dict[str, Any]) -> str:
    """Returns a logged in user's token"""
    login_payload = {
        'email': test_user['email'],
        'password': test_user['password']
    }
    res = test_client.post("user/login", json=login_payload)
    return res.json()['data']['token']


def gen_payload(name: str | None = None):
    """Creates a randomly generated user payload"""
    if name == None:
        name = uuid4().hex[:5]
    return \
    {
        'email': f'{name}@test.com',
        'phone': '3476538334',
        'password': 'test',
        'firstName': 'Ben',
        'lastName': 'Dover',
    }
