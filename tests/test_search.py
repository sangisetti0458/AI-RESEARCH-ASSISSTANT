from unittest.mock import patch

from .conftest import client


@patch("app.api.search_routes.semantic_search")
def test_semantic_search(mock_search):

    mock_search.return_value = {
        "ids": [["1"]],
        "documents": [["Artificial Intelligence is a branch of Computer Science."]],
        "metadatas": [[
            {
                "document_id": 1,
                "file_name": "AI.pdf",
                "page_number": 1,
            }
        ]],
        "distances": [[0.12]],
    }

    response = client.post(
        "/search/",
        json={
            "query": "What is Artificial Intelligence?",
            "top_k": 5,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "documents" in data
    assert "metadatas" in data
    assert "ids" in data


@patch("app.api.search_routes.semantic_search")
def test_empty_search_results(mock_search):

    mock_search.return_value = {
        "ids": [[]],
        "documents": [[]],
        "metadatas": [[]],
        "distances": [[]],
    }

    response = client.post(
        "/search/",
        json={
            "query": "This document does not exist",
            "top_k": 5,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["documents"] == [[]]