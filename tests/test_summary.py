from unittest.mock import patch

from .conftest import client


@patch("app.services.summary_service.SummaryService.summarize_document")
def test_summary(mock_summary):

    mock_summary.return_value = {
        "document_id": 1,
        "summary": "This document explains Artificial Intelligence.",
        "key_points": [
            "AI definition",
            "Machine Learning",
            "Deep Learning",
            "Applications",
            "Future scope",
        ],
    }

    response = client.get("/documents/1/summarize")

    assert response.status_code == 200

    data = response.json()

    assert data["document_id"] == 1

    assert "Artificial Intelligence" in data["summary"]

    assert len(data["key_points"]) == 5


@patch("app.services.summary_service.SummaryService.summarize_document")
def test_summary_document_not_found(mock_summary):

    mock_summary.return_value = {
        "document_id": 99,
        "summary": "Document not found.",
        "key_points": [],
    }

    response = client.get("/documents/99/summarize")

    assert response.status_code == 200

    data = response.json()

    assert data["summary"] == "Document not found."

    assert data["key_points"] == []