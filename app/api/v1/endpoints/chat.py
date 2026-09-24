from fastapi import APIRouter, HTTPException
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.rag_service import rag_service

router = APIRouter()


@router.post("/query", response_model=ChatResponse)
async def query_rag(request: ChatRequest):
    """
    Query the document knowledge base using RAG pipeline with PGVector retrieval.
    """
    try:
        response = rag_service.query(question=request.query, k=request.k)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
