from unittest.mock import patch

from .conftest import client


@patch("app.services.compare_service.CompareService.compare_documents")
def test_compare_documents(mock_compare):

    mock_compare.return_value = {
        "document_1": "AI.pdf",
        "document_2": "ML.pdf",
        "summary": "Both documents discuss Artificial Intelligence.",
        "similarities": [
            "Both discuss AI",
            "Both explain algorithms",
        ],
        "differences": [
            "ML focuses on learning",
            "AI is broader",
        ],
    }

    response = client.post(
        "/documents/compare",
        json={
            "document_id_1": 1,
            "document_id_2": 2,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["document_1"] == "AI.pdf"

    assert data["document_2"] == "ML.pdf"

    assert len(data["similarities"]) == 2

    assert len(data["differences"]) == 2


@patch("app.services.compare_service.CompareService.compare_documents")
def test_compare_same_document(mock_compare):

    mock_compare.return_value = {
        "document_1": "AI.pdf",
        "document_2": "AI.pdf",
        "summary": "Documents are identical.",
        "similarities": [
            "Same content",
        ],
        "differences": [],
    }

    response = client.post(
        "/documents/compare",
        json={
            "document_id_1": 1,
            "document_id_2": 1,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["document_1"] == "AI.pdf"

    assert len(data["differences"]) == 0