from pydantic import BaseModel


class TopQueriedDocument(BaseModel):
    document_name: str
    query_count: int


class AnalyticsResponse(BaseModel):

    total_documents: int

    total_chunks: int

    total_embeddings: int

    total_questions: int

    category_distribution: dict[str, int]

    top_queried_documents: list[TopQueriedDocument]