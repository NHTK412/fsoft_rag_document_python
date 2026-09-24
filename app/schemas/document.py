from pydantic import BaseModel
from typing import Optional, Dict, Any


class DocumentUploadResponse(BaseModel):
    filename: str
    chunks_created: int
    message: str
    metadata: Optional[Dict[str, Any]] = None
