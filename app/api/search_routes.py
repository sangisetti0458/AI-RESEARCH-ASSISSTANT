from fastapi import APIRouter

from app.schemas.search_schema import SearchRequest
from app.utils.search_engine import semantic_search

router = APIRouter(
    prefix="/search",
    tags=["Semantic Search"]
)


@router.post("/")
def search_documents(request: SearchRequest):
    results = semantic_search(
        request.query,
        request.top_k
    )

    return results