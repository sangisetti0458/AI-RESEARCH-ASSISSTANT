from pydantic import BaseModel


class CompareRequest(BaseModel):
    document_id_1: int
    document_id_2: int


class CompareResponse(BaseModel):
    document_1: str
    document_2: str
    similarities: list[str]
    differences: list[str]
    summary: str