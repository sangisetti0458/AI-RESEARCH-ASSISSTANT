import os
import shutil
from datetime import datetime

from sqlalchemy.orm import Session

from app.database.models import Document
from app.utils.pdf_processor import extract_text_from_pdf
from app.utils.text_chunker import split_pages_into_chunks
from app.utils.embedding_generator import generate_embeddings
from app.utils.vector_store import (
    store_embeddings,
    delete_embeddings,
)

# NEW IMPORT
from app.ml.predict import predict_category

UPLOAD_DIR = "data/documents"

os.makedirs(UPLOAD_DIR, exist_ok=True)


class DocumentService:

    @staticmethod
    def save_document(file, db: Session):

        file_path = os.path.join(UPLOAD_DIR, file.filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Extract PDF pages
        pages = extract_text_from_pdf(file_path)

        # Combine all pages into one text
        full_text = "\n".join(
            page["text"] for page in pages
        )

        # Predict category using TensorFlow
        prediction = predict_category(full_text)

        predicted_category = prediction["category"]

        print(f"\nPredicted Category: {predicted_category}")
        print(f"Confidence: {prediction['confidence']}\n")

        # Chunking
        chunks = split_pages_into_chunks(pages)

        # Generate embeddings
        embeddings = generate_embeddings(chunks)

        # Save document
        document = Document(
            document_name=file.filename,
            upload_time=datetime.utcnow(),
            total_pages=len(pages),
            total_chunks=len(chunks),
            category=predicted_category,
            processing_status="COMPLETED",
            file_path=file_path,
        )

        db.add(document)
        db.commit()
        db.refresh(document)

        # Store embeddings
        store_embeddings(
            document.id,
            document.document_name,
            chunks,
            embeddings,
        )

        return document

    @staticmethod
    def get_all_documents(db: Session):

        return (
            db.query(Document)
            .order_by(Document.upload_time.desc())
            .all()
        )

    @staticmethod
    def get_document_by_id(document_id: int, db: Session):

        document = (
            db.query(Document)
            .filter(Document.id == document_id)
            .first()
        )

        if not document:
            raise ValueError("Document not found.")

        return document

    @staticmethod
    def delete_document(document_id: int, db: Session):

        document = (
            db.query(Document)
            .filter(Document.id == document_id)
            .first()
        )

        if not document:
            raise ValueError("Document not found.")

        if document.file_path and os.path.exists(document.file_path):
            os.remove(document.file_path)

        delete_embeddings(document.id)

        db.delete(document)
        db.commit()

        return {
            "message": "Document deleted successfully."
        }

    @staticmethod
    def reprocess_document(document_id: int, db: Session):

        document = (
            db.query(Document)
            .filter(Document.id == document_id)
            .first()
        )

        if not document:
            raise ValueError("Document not found.")

        if not os.path.exists(document.file_path):
            raise ValueError("PDF file not found.")

        document.processing_status = "PROCESSING"
        db.commit()

        pages = extract_text_from_pdf(document.file_path)

        full_text = "\n".join(
            page["text"] for page in pages
        )

        prediction = predict_category(full_text)

        chunks = split_pages_into_chunks(pages)

        embeddings = generate_embeddings(chunks)

        delete_embeddings(document.id)

        store_embeddings(
            document.id,
            document.document_name,
            chunks,
            embeddings,
        )

        document.total_pages = len(pages)
        document.total_chunks = len(chunks)
        document.category = prediction["category"]
        document.processing_status = "COMPLETED"
        document.upload_time = datetime.utcnow()

        db.commit()
        db.refresh(document)

        return document