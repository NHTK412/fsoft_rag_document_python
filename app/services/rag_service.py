from typing import List, Optional
from langchain_core.documents import Document

from app.services import vector_store
from app.services.llm_factory import get_llm
from app.schemas.chat import RAGAnswerWithCitations
from app.prompts.rag_prompts import rag_prompt


def format_context_with_sources(documents: List[Document]) -> str:
    """Format retrieved document chunks with clear source and location citations."""
    formatted_chunks = []

    for idx, doc in enumerate(documents, start=1):
        source = doc.metadata.get("source", "Không rõ tên file")

        # Xác định vị trí: Trang PDF hoặc Mốc thời gian Video hoặc Excel sheet
        if "display_page" in doc.metadata or "page" in doc.metadata:
            page = doc.metadata.get("display_page", doc.metadata.get("page", 0))
            location = f"Trang {page}"
        elif "timestamp" in doc.metadata:
            location = f"Phút {doc.metadata.get('timestamp')}"
        elif "sheet_name" in doc.metadata:
            location = f"Sheet: {doc.metadata.get('sheet_name')} - Dòng {doc.metadata.get('row_index')}"
        else:
            location = "Toàn bộ tài liệu"

        chunk_text = (
            f"--- [NGUỒN {idx}] ---\n"
            f"Tệp: {source} | Vị trí: {location}\n"
            f"Nội dung:\n{doc.page_content}\n"
        )
        formatted_chunks.append(chunk_text)

    return "\n".join(formatted_chunks)


def ask_document(question: str, project_id: str, sources: Optional[List[str]] = None) -> RAGAnswerWithCitations:
    """
    RAG QA pipeline:
    1. Similarity search in PGVector filtered by project_id and optional sources
    2. Format context with source citations
    3. Call Gemini with Structured Output
    """
    # 1. Build filter
    filter_dict = {"project_id": str(project_id)}
    if sources and len(sources) > 0:
        if len(sources) == 1:
            filter_dict["source"] = sources[0]
        else:
            filter_dict["source"] = {"$in": sources}

    # Retrieve relevant chunks
    relevant_docs = vector_store.get_vector_store().similarity_search(
        query=question,
        k=4,
        filter=filter_dict
    )

    if not relevant_docs:
        return RAGAnswerWithCitations(
            answer="Không tìm thấy tài liệu phù hợp trong danh sách tài liệu đã chọn của dự án này.",
            citations=[]
        )

    # 2. Format context
    formatted_context = format_context_with_sources(relevant_docs)

    # 3. Format prompt
    formatted_prompt = rag_prompt.format_messages(
        context=formatted_context,
        question=question
    )

    # 4. Generate structured answer with Gemini (temperature=0 for factual accuracy)
    llm = get_llm(temperature=0)
    structured_llm = llm.with_structured_output(RAGAnswerWithCitations)
    response = structured_llm.invoke(formatted_prompt)

    return response
