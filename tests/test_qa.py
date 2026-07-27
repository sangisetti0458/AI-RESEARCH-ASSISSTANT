from unittest.mock import patch

from .conftest import client


@patch("app.services.rag_service.RAGService.ask_question")
def test_ask_question(mock_ask):

    mock_ask.return_value = {
        "answer": "Artificial Intelligence is the simulation of human intelligence by machines.",
        "citations": [
            {
                "file_name": "AI.pdf",
                "page_number": 1,
            }
        ],
    }

    response = client.post(
        "/ask/",
        json={
            "session_id": "session123",
            "question": "What is Artificial Intelligence?",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["answer"].startswith("Artificial Intelligence")

    assert len(data["citations"]) == 1

    assert data["citations"][0]["file_name"] == "AI.pdf"


@patch("app.services.rag_service.RAGService.ask_question")
def test_ask_question_no_answer(mock_ask):

    mock_ask.return_value = {
        "answer": "I cannot determine the answer from the provided documents.",
        "citations": [],
    }

    response = client.post(
        "/ask/",
        json={
            "session_id": "session123",
            "question": "Who invented teleportation?",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert (
        data["answer"]
        == "I cannot determine the answer from the provided documents."
    )

    assert data["citations"] == []