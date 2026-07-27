from pydantic import BaseModel


class QuestionRequest(BaseModel):
    session_id: str
    question: str


class Citation(BaseModel):
    file_name: str
    page_number: int


class RetrievedContext(BaseModel):
    file_name: str
    page_number: int
    content: str


class QuestionResponse(BaseModel):
    answer: str
    citations: list[Citation]
    confidence_score: float
    retrieved_context: list[RetrievedContext]