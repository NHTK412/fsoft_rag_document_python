from app.core.config import settings
import psycopg
from typing import List
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.services.vector_store import get_vector_store
from app.services.document_loader import load_and_parse_document


def split_documents(documents: List[Document], chunk_size: int = 800, chunk_overlap: int = 150) -> List[Document]:
    """Split documents into smaller chunks and tag chunk_id."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", " ", ""]
    )

    chunks = text_splitter.split_documents(documents)

    for index, chunk in enumerate(chunks):
        source = chunk.metadata.get("source", "unknown")
        page = chunk.metadata.get("display_page", chunk.metadata.get("page", 0))
        chunk.metadata["chunk_id"] = f"{source}_p{page}_chunk_{index}"

    return chunks


def save_to_vector_db(chunks: List[Document]):
    """Save document chunks to PGVector store."""
    vector_store = get_vector_store()
    vector_store.add_documents(chunks)


def process_and_index_file(bucket_name: str, object_name: str, project_id: str) -> int:
    """
    Main workflow:
    1. Download from MinIO & parse into documents
    2. Split into chunks
    3. Index into PGVector
    Returns: total number of chunks indexed.
    """
    docs = load_and_parse_document(bucket_name, object_name, project_id)
    chunks = split_documents(docs)
    save_to_vector_db(chunks)
    return len(chunks)

def delete_document(object_name: str, project_id: str):
    sql = """
        DELETE FROM langchain_pg_embedding
        WHERE cmetadata->>'source' = %s
            AND cmetadata->>'project_id' = %s
    """
    with psycopg.connect(conninfo=settings.DB_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (object_name, project_id))
            conn.commit()

