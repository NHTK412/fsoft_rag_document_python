from sqlalchemy import create_engine, text
from app.core.config import settings

engine = create_engine(settings.database_url)


def init_db():
    """Ensure vector extension is created in PostgreSQL."""
    with engine.connect() as connection:
        connection.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
        connection.commit()
