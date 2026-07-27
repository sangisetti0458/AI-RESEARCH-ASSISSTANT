from fastapi import FastAPI

from app.database.database import engine
from app.database.models import Base

from app.api.document_routes import router as document_router
from app.api.search_routes import router as search_router
from app.api.qa_routes import router as qa_router
from app.api.summary_routes import router as summary_router
from app.api.compare_routes import router as compare_router
from app.api.analytics_routes import router as analytics_router

from app.core.logger import logger

# Create database tables
Base.metadata.create_all(bind=engine)

logger.info("Application started successfully.")

app = FastAPI(
    title="AI Research & Knowledge Assistant",
    description="Backend API for AI-powered document retrieval and question answering.",
    version="1.0.0",
)

# Register API routes
app.include_router(document_router)
app.include_router(search_router)
app.include_router(qa_router)
app.include_router(summary_router)
app.include_router(compare_router)
app.include_router(analytics_router)


@app.get("/")
def root():
    logger.info("Root endpoint accessed.")
    return {
        "message": "Welcome to AI Research & Knowledge Assistant"
    }


@app.get("/health")
def health():
    logger.info("Health endpoint accessed.")
    return {
        "status": "healthy"
    }