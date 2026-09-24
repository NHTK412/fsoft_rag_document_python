from langchain_postgres import PGVector
from app.core.config import settings
from app.services.llm_factory import get_embedding_model


def get_vector_store() -> PGVector:
    """Initialize and return LangChain PGVector instance."""
    embeddings = get_embedding_model()
    return PGVector(
        embeddings=embeddings,
        collection_name=settings.PGVECTOR_COLLECTION_NAME,
        connection=settings.sync_connection_string,
        use_jsonb=True,
    )


def init_vector_store():
    """Ensure PGVector extension and tables are initialized."""
    vector_store = get_vector_store()
    vector_store.create_tables_if_not_exists()
