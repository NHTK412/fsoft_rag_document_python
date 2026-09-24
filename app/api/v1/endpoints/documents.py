from app.schemas.document import DeleteRequest
from fastapi import APIRouter, HTTPException
from app.schemas.document import UploadFileRequest, UploadFileResponse
from app.services import document_service

router = APIRouter()


@router.post("/upload", response_model=UploadFileResponse)
def upload_file(request: UploadFileRequest):
    """
    Tải file từ MinIO, bóc tách nội dung, chia chunks và lưu vector vào PGVector.
    """
    try:
        total_chunks = document_service.process_and_index_file(
            bucket_name=request.bucket_name,
            object_name=request.object_name,
            project_id=request.project_id
        )
        return UploadFileResponse(
            status="success",
            project_id=request.project_id,
            object_name=request.object_name,
            total_chunks=total_chunks,
            message=f"Đã xử lý và nạp thành công {total_chunks} chunks vào PGVector."
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/delete", status_code=204)
def delete_document(request: DeleteRequest):
    try:
        document_service.delete_document(
            object_name=request.object_name,
            project_id=request.project_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))