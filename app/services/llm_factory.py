from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from app.core.config import settings


def get_embedding_model() -> GoogleGenerativeAIEmbeddings:
    """Return LangChain Google Gemini Embeddings model."""
    return GoogleGenerativeAIEmbeddings(
        model=settings.EMBEDDING_MODEL_NAME,
        google_api_key=settings.GOOGLE_API_KEY
    )


def get_llm(temperature: float = 0.2) -> ChatGoogleGenerativeAI:
    """Return LangChain ChatGoogleGenerativeAI instance."""
    return ChatGoogleGenerativeAI(
        model=settings.GEMINI_MODEL_NAME,
        temperature=temperature,
        google_api_key=settings.GOOGLE_API_KEY
    )

