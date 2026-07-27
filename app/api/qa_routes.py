from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.dependencies import get_db

from app.schemas.question_schema import (
    QuestionRequest,
    QuestionResponse,
)

from app.services.rag_service import RAGService

router = APIRouter(
    prefix="/ask",
    tags=["Question Answering"],
)


@router.post("/", response_model=QuestionResponse)
def ask_question(
    request: QuestionRequest,
    db: Session = Depends(get_db),
):

    return RAGService.ask_question(
        db=db,
        session_id=request.session_id,
        question=request.question,
    )