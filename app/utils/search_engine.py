from app.utils.embedding_generator import model
from app.utils.vector_store import collection


def semantic_search(query: str, top_k: int = 5):
    """
    Search ChromaDB for the most relevant chunks.
    """

    query_embedding = model.encode(query)

    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=top_k
    )

    return results