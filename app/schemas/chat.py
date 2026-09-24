from pydantic import BaseModel, Field
from typing import List


class ChatRequest(BaseModel):
    query: str = Field(..., description="Câu hỏi của người dùng", min_length=1)
    project_id: str = Field(..., description="ID dự án cần tra cứu tài liệu")


class CitationItem(BaseModel):
    """Mô tả một nguồn trích dẫn hỗ trợ cho câu trả lời"""
    source_file: str = Field(description="Tên file tài liệu gốc (VD: Deployment_Guide.pdf)")
    location: str = Field(description="Vị trí trích dẫn, ví dụ: 'Trang 4' hoặc 'Phút 02:15' hoặc 'Sheet 1 - Dòng 12'")
    quote: str = Field(description="Đoạn văn ngắn nguyên văn làm bằng chứng chứng minh thông tin")


class RAGAnswerWithCitations(BaseModel):
    """Cấu trúc dữ liệu phản hồi cuối cùng của hệ thống RAG"""
    answer: str = Field(description="Nội dung câu trả lời đầy đủ, chi tiết và chính xác cho câu hỏi của người dùng")
    citations: List[CitationItem] = Field(default=[], description="Danh sách các nguồn tài liệu được sử dụng để tổng hợp câu trả lời")
