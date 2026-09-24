import os
import tempfile
from contextlib import contextmanager
from typing import List
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader
from app.core.minio_client import minio_client


@contextmanager
def load_file_from_minio(bucket_name: str, object_name: str):
    """
    Context manager to download a file from MinIO to a temporary file on disk,
    and automatically remove it upon completion.
    """
    ext = object_name.split(".")[-1]
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=f".{ext}")
    temp_path = temp_file.name
    temp_file.close()

    try:
        minio_client.fget_object(bucket_name, object_name, temp_path)
        yield temp_path
    except Exception as e:
        print(f"Error when downloading {object_name} from MinIO bucket {bucket_name}: {e}")
        raise e
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


def parse_pdf(file_path: str, origin_name: str, project_id: str) -> List[Document]:
    """Parse PDF file using PyPDFLoader and enrich metadata."""
    loader = PyPDFLoader(file_path)
    docs = loader.load()

    for doc in docs:
        doc.metadata["project_id"] = project_id
        doc.metadata["source"] = origin_name
        doc.metadata["display_page"] = doc.metadata.get("page", 0) + 1
    return docs


def load_and_parse_document(bucket_name: str, object_name: str, project_id: str) -> List[Document]:
    """Load file from MinIO and parse into LangChain Documents based on file extension."""
    ext = object_name.split(".")[-1].lower()
    with load_file_from_minio(bucket_name, object_name) as file_path:
        if ext == "pdf":
            docs = parse_pdf(file_path, object_name, project_id)
        elif ext == "docx":
            # Placeholder cho docx sau này
            raise NotImplementedError("DOCX parsing will be implemented soon.")
        else:
            raise ValueError(f"Unsupported file type: {ext}")
    return docs
