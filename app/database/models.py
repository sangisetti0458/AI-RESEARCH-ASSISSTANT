from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime

from app.database.database import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)

    document_name = Column(String, nullable=False)

    upload_time = Column(DateTime, default=datetime.utcnow)

    total_pages = Column(Integer, default=0)

    total_chunks = Column(Integer, default=0)

    category = Column(String, default="Unknown")

    processing_status = Column(String, default="PROCESSING")

    file_path = Column(String)


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)

    session_id = Column(String, index=True)

    role = Column(String)

    message = Column(Text)

    created_at = Column(DateTime, default=datetime.utcnow)


class QueryLog(Base):
    __tablename__ = "query_logs"

    id = Column(Integer, primary_key=True, index=True)

    session_id = Column(String, index=True)

    question = Column(Text, nullable=False)

    document_name = Column(String, nullable=False)

    page_number = Column(Integer)

    created_at = Column(DateTime, default=datetime.utcnow)