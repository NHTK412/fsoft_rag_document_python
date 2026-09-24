from fastapi import APIRouter
from app.api.v1.endpoints import documents, chat

api_router = APIRouter()

# Primary RESTful routes
api_router.include_router(documents.router, prefix="/documents", tags=["documents"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])

# Backward-compatible aliases for previous paths (/upload and /ask)
api_router.include_router(documents.router, prefix="/upload", tags=["documents"], include_in_schema=False)
api_router.include_router(chat.router, prefix="/ask", tags=["chat"], include_in_schema=False)