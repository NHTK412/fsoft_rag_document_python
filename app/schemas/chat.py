from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class ChatRequest(BaseModel):
    query: str = Field(..., description="User query or question", min_length=1)
    k: int = Field(default=4, description="Number of context chunks to retrieve", ge=1, le=20)


class SourceDocument(BaseModel):
    content: str
    metadata: Dict[str, Any] = {}


class ChatResponse(BaseModel):
    query: str
    answer: str
    sources: List[SourceDocument] = []
