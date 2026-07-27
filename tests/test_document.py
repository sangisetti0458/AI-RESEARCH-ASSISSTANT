from io import BytesIO
from unittest.mock import patch

from .conftest import client


@patch("app.services.document_service.DocumentService.save_document")
def test_upload_pdf(mock_save):

    mock_save.return_value = {
        "id": 1,
        "document_name": "sample.pdf",
        "upload_time": "2026-07-27T00:00:00",
        "total_pages": 5,
        "total_chunks": 10,
        "category": "Computer Engineering",
        "processing_status": "COMPLETED",
        "file_path": "data/documents/sample.pdf",
    }

    response = client.post(
        "/documents/upload",
        files={
            "file": (
                "sample.pdf",
                BytesIO(b"Dummy PDF Content"),
                "application/pdf",
            )
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["document_name"] == "sample.pdf"
    assert data["processing_status"] == "COMPLETED"


def test_upload_invalid_file():

    response = client.post(
        "/documents/upload",
        files={
            "file": (
                "sample.txt",
                BytesIO(b"Hello"),
                "text/plain",
            )
        },
    )

    assert response.status_code == 400

    assert response.json()["detail"] == "Only PDF files are allowed."


@patch("app.services.document_service.DocumentService.get_all_documents")
def test_get_documents(mock_documents):

    mock_documents.return_value = []

    response = client.get("/documents")

    assert response.status_code == 200

    assert response.json() == []


@patch("app.services.document_service.DocumentService.get_document_by_id")
def test_get_document(mock_document):

    mock_document.return_value = {
        "id": 1,
        "document_name": "sample.pdf",
        "upload_time": "2026-07-27T00:00:00",
        "total_pages": 5,
        "total_chunks": 10,
        "category": "Computer Engineering",
        "processing_status": "COMPLETED",
        "file_path": "data/documents/sample.pdf",
    }

    response = client.get("/documents/1")

    assert response.status_code == 200

    assert response.json()["id"] == 1


@patch("app.services.document_service.DocumentService.delete_document")
def test_delete_document(mock_delete):

    mock_delete.return_value = {
        "message": "Document deleted successfully."
    }

    response = client.delete("/documents/1")

    assert response.status_code == 200

    assert response.json()["message"] == "Document deleted successfully."


@patch("app.services.document_service.DocumentService.reprocess_document")
def test_reprocess_document(mock_reprocess):

    mock_reprocess.return_value = {
        "id": 1,
        "document_name": "sample.pdf",
        "upload_time": "2026-07-27T00:00:00",
        "total_pages": 5,
        "total_chunks": 10,
        "category": "Computer Engineering",
        "processing_status": "COMPLETED",
        "file_path": "data/documents/sample.pdf",
    }

    response = client.post("/documents/1/reprocess")

    assert response.status_code == 200

    assert response.json()["processing_status"] == "COMPLETED"