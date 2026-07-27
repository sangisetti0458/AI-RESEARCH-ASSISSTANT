from .conftest import client


def test_root():

    response = client.get("/")

    assert response.status_code == 200

    assert response.json() == {
        "message": "Welcome to AI Research & Knowledge Assistant"
    }


def test_health():

    response = client.get("/health")

    assert response.status_code == 200

    assert response.json() == {
        "status": "healthy"
    }