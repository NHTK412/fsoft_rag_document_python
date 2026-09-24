from pydantic import BaseModel, Field


class UploadFileRequest(BaseModel):
    project_id: str = Field(..., description="ID dự án sở hữu tài liệu")
    object_name: str = Field(..., description="Tên file/đường dẫn object trong MinIO")
    bucket_name: str = Field(..., description="Tên bucket chứa file trong MinIO")


class UploadFileResponse(BaseModel):
    status: str = "success"
    project_id: str
    object_name: str
    total_chunks: int
    message: str
