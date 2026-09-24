import os
import shutil
from pathlib import Path
from typing import List
from fastapi import UploadFile, HTTPException

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, TextLoader

from app.core.config import settings
from app.services.vector_store import get_vector_store

UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


class DocumentService:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP,
            separators=["\n\n", "\n", " ", ""]
        )

    def save_upload_file(self, file: UploadFile) -> Path:
        """Save uploaded file to local disk."""
        file_path = UPLOAD_DIR / file.filename
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return file_path

    def load_document(self, file_path: Path) -> List[Document]:
        """Load document based on file extension."""
        ext = file_path.suffix.lower()
        if ext == ".pdf":
            loader = PyPDFLoader(str(file_path))
        elif ext in [".txt", ".md"]:
            loader = TextLoader(str(file_path), encoding="utf-8")
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file format: {ext}. Only .pdf, .txt, and .md are supported."
            )
        return loader.load()

    def process_and_index_document(self, file: UploadFile) -> int:
        """Save, split, and add document chunks to PGVector."""
        saved_path = self.save_upload_file(file)
        docs = self.load_document(saved_path)

        # Enrich metadata
        for doc in docs:
            doc.metadata["source_filename"] = file.filename

        # Split into chunks
        chunks = self.text_splitter.split_documents(docs)

        if not chunks:
            raise HTTPException(status_code=400, detail="The document contains no readable text.")

        # Ingest into PGVector
        vector_store = get_vector_store()
        vector_store.add_documents(chunks)

        return len(chunks)


document_service = DocumentService()
