from typing import List, Dict, Any
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from app.services.vector_store import get_vector_store
from app.services.llm_factory import get_llm
from app.schemas.chat import ChatResponse, SourceDocument

RAG_PROMPT_TEMPLATE = """You are a helpful assistant. Use the following pieces of retrieved context to answer the question.
If you do not know the answer, say that you don't know based on the provided documents. Keep the answer concise and accurate.

Context:
{context}

Question:
{question}

Answer:"""


class RAGService:
    def __init__(self):
        self.prompt = ChatPromptTemplate.from_template(RAG_PROMPT_TEMPLATE)
        self.output_parser = StrOutputParser()

    def query(self, question: str, k: int = 4) -> ChatResponse:
        vector_store = get_vector_store()
        retriever = vector_store.as_retriever(search_kwargs={"k": k})

        # Retrieve relevant chunks
        docs = retriever.invoke(question)

        # Format context string
        context_text = "\n\n---\n\n".join([doc.page_content for doc in docs])

        # Generate response with LLM
        llm = get_llm()
        chain = self.prompt | llm | self.output_parser
        answer = chain.invoke({"context": context_text, "question": question})

        # Format source documents
        sources = [
            SourceDocument(content=doc.page_content, metadata=doc.metadata)
            for doc in docs
        ]

        return ChatResponse(
            query=question,
            answer=answer,
            sources=sources
        )


rag_service = RAGService()
