from typing import List

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Path
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.schemas.document_schema import DocumentResponse
from app.services.document_service import DocumentService

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)


@router.post("/upload", response_model=DocumentResponse)
def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed."
        )

    return DocumentService.save_document(file, db)


@router.get("", response_model=List[DocumentResponse])
def get_documents(db: Session = Depends(get_db)):
    return DocumentService.get_all_documents(db)


@router.get("/{document_id}", response_model=DocumentResponse)
def get_document(
    document_id: int = Path(..., gt=0),
    db: Session = Depends(get_db)
):

    try:
        return DocumentService.get_document_by_id(document_id, db)

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )


@router.delete("/{document_id}")
def delete_document(
    document_id: int,
    db: Session = Depends(get_db)
):

    try:
        return DocumentService.delete_document(document_id, db)

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )


@router.post("/{document_id}/reprocess", response_model=DocumentResponse)
def reprocess_document(
    document_id: int,
    db: Session = Depends(get_db)
):

    try:
        return DocumentService.reprocess_document(document_id, db)

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )