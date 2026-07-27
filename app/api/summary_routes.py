from fastapi import APIRouter

from app.schemas.summary_schema import SummaryResponse
from app.services.summary_service import SummaryService

router = APIRouter(
    prefix="/documents",
    tags=["Document Summarization"]
)


@router.get("/{document_id}/summarize", response_model=SummaryResponse)
def summarize(document_id: int):

    return SummaryService.summarize_document(document_id)