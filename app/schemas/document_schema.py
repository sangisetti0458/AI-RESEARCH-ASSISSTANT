from datetime import datetime

from pydantic import BaseModel


class DocumentResponse(BaseModel):
    id: int
    document_name: str
    upload_time: datetime
    total_pages: int
    total_chunks: int
    processing_status: str
    category: str

    class Config:
        from_attributes = True