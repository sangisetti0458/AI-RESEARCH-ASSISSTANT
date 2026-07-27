from pydantic import BaseModel


class SummaryResponse(BaseModel):
    document_id: int
    executive_summary: str
    technical_summary: str
    bullet_point_summary: list[str]
    key_takeaways: list[str]