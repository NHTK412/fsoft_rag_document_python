from fastapi import APIRouter, UploadFile, File, HTTPException
from app.schemas.document import DocumentUploadResponse
from app.services.document_service import document_service

router = APIRouter()


@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(file: UploadFile = File(...)):
    """
    Upload and index a document (.pdf, .txt, .md) into PGVector.
    """
    try:
        chunks_count = document_service.process_and_index_document(file)
        return DocumentUploadResponse(
            filename=file.filename or "unknown",
            chunks_created=chunks_count,
            message=f"Document successfully indexed into {chunks_count} chunks."
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
