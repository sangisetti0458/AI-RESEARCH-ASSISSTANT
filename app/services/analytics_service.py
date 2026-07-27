from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database.models import (
    Document,
    Conversation,
    QueryLog,
)


class AnalyticsService:

    @staticmethod
    def get_statistics(db: Session):

        # Total uploaded documents
        total_documents = db.query(Document).count()

        # Total chunks
        total_chunks = (
            db.query(func.sum(Document.total_chunks))
            .scalar()
        )

        if total_chunks is None:
            total_chunks = 0

        # Every chunk has one embedding
        total_embeddings = total_chunks

        # Total questions asked
        total_questions = (
            db.query(Conversation)
            .filter(Conversation.role == "user")
            .count()
        )

        # Category distribution
        categories = (
            db.query(
                Document.category,
                func.count(Document.id)
            )
            .group_by(Document.category)
            .all()
        )

        category_distribution = {
            category: count
            for category, count in categories
        }

        # Top queried documents
        top_documents = (
            db.query(
                QueryLog.document_name,
                func.count(QueryLog.id).label("query_count")
            )
            .group_by(QueryLog.document_name)
            .order_by(func.count(QueryLog.id).desc())
            .limit(5)
            .all()
        )

        top_queried_documents = [
            {
                "document_name": document_name,
                "query_count": query_count,
            }
            for document_name, query_count in top_documents
        ]

        return {
            "total_documents": total_documents,
            "total_chunks": total_chunks,
            "total_embeddings": total_embeddings,
            "total_questions": total_questions,
            "category_distribution": category_distribution,
            "top_queried_documents": top_queried_documents,
        }