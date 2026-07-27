from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.dependencies import get_db

from app.schemas.analytics_schema import AnalyticsResponse

from app.services.analytics_service import AnalyticsService

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"],
)


@router.get(
    "/",
    response_model=AnalyticsResponse,
)
def get_analytics(
    db: Session = Depends(get_db),
):

    return AnalyticsService.get_statistics(db)