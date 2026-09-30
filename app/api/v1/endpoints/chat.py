from fastapi import APIRouter, HTTPException
from app.schemas.chat import ChatRequest, RAGAnswerWithCitations
from app.services import rag_service

router = APIRouter()


@router.post("/", response_model=RAGAnswerWithCitations)
def chat_with_document(request: ChatRequest):
    """
    Hỏi đáp dựa trên tài liệu đã được index trong dự án (RAG with Citations).
    """
    try:
        response = rag_service.ask_document(
            question=request.query,
            project_id=request.project_id,
            sources=request.sources
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
