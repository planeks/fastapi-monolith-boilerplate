import pytest
from starlette.testclient import TestClient

from src.app import app


@pytest.fixture()
def client():
    return TestClient(app)


def test_app_exists():
    assert app is not None


def test_docs_reachable(client):
    response = client.get("/docs")
    assert response.status_code == 200


def test_root_no_server_error(client):
    response = client.get("/")
    assert response.status_code < 500
