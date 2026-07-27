from unittest.mock import patch

from .conftest import client


@patch("app.services.analytics_service.AnalyticsService.get_statistics")
def test_analytics(mock_stats):

    mock_stats.return_value = {
        "total_documents": 8,
        "total_chunks": 21,
        "total_questions": 15,
        "category_distribution": {
            "Computer Engineering": 3,
            "Unknown": 5,
        },
        "top_queried_documents": [
            {
                "document_name": "AI.pdf",
                "query_count": 8,
            },
            {
                "document_name": "ML.pdf",
                "query_count": 4,
            },
        ],
    }

    response = client.get("/analytics/")

    assert response.status_code == 200

    data = response.json()

    assert data["total_documents"] == 8

    assert data["total_chunks"] == 21

    assert data["total_questions"] == 15

    assert len(data["top_queried_documents"]) == 2

    assert (
        data["top_queried_documents"][0]["document_name"]
        == "AI.pdf"
    )