from fastapi import APIRouter, HTTPException

from app.schemas.compare_schema import (
    CompareRequest,
    CompareResponse
)
from app.services.compare_service import CompareService

router = APIRouter(
    prefix="/documents",
    tags=["Document Comparison"]
)


@router.post(
    "/compare",
    response_model=CompareResponse
)
def compare_documents(request: CompareRequest):

    try:
        return CompareService.compare_documents(
            request.document_id_1,
            request.document_id_2
        )

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )