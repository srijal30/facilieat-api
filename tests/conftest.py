import os
from typing import Any, Dict
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from src.app import app


@pytest.fixture(scope='session', autouse=True)
def database_management():
    os.system("rm data.sqlite")
    os.system("prisma db push")
    yield


@pytest.fixture()
def test_client() -> TestClient:
    with TestClient(app) as client:
        yield client


@pytest.fixture()
def test_user(test_client: TestClient) -> Dict[str, Any]:
    create_payload = gen_payload()
    test_client.post("user/create", json=create_payload)
    yield create_payload


def gen_payload(name: str | None = None):
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
