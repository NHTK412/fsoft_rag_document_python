# RAG Document Service with FastAPI + LangChain + PGVector + Google Gemini

Dự án RAG (Retrieval-Augmented Generation) phục vụ hỏi đáp trên tài liệu (.pdf, .txt, .md), sử dụng:
- **FastAPI**: Xây dựng RESTful API tốc độ cao, hỗ trợ Swagger UI trực quan.
- **Google Gemini & Embeddings**: Sử dụng `gemini-1.5-flash` và `models/text-embedding-004` (thông qua `langchain-google-genai`).
- **LangChain & langchain-postgres**: Quản lý pipeline RAG, text splitters và vector store.
- **PostgreSQL + PGVector**: Lưu trữ và tìm kiếm vector tương đồng (vector similarity search).

---

## 📁 Cấu trúc thư mục (Directory Structure)

```text
rag_document/
├── app/
│   ├── __init__.py
│   ├── main.py                     # Entry point FastAPI, CORS, Lifespan init DB
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py               # Pydantic BaseSettings quản lý biến môi trường
│   │   └── database.py             # Kết nối SQLAlchemy & kích hoạt extension pgvector
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── router.py           # Gom nhóm tất cả endpoints v1
│   │       └── endpoints/
│   │           ├── __init__.py
│   │           ├── documents.py    # API Upload & index tài liệu
│   │           └── chat.py         # API Hỏi đáp (Query RAG)
│   ├── schemas/                    # Pydantic Schemas (Request/Response models)
│   │   ├── __init__.py
│   │   ├── chat.py                 # Schemas cho ChatRequest, ChatResponse
│   │   └── document.py             # Schemas cho DocumentUploadResponse
│   └── services/                   # Business logic & LangChain pipeline
│       ├── __init__.py
│       ├── llm_factory.py          # Khởi tạo Chat LLM & Embedding models
│       ├── vector_store.py         # Cấu hình PGVector (langchain-postgres)
│       ├── document_service.py     # Đọc file, chunking (TextSplitter), nhúng vào PGVector
│       └── rag_service.py          # Pipeline RAG retrieval + LLM question-answering
├── data/
│   └── uploads/                    # Thư mục lưu file tạm khi người dùng tải lên
├── docker-compose.yml              # File docker chạy PostgreSQL có sẵn PGVector
├── .env.example                    # File mẫu cấu hình biến môi trường
├── .gitignore                      # Git ignore
├── requirements.txt                # Thư viện phụ thuộc
└── README.md                       # Tài liệu hướng dẫn
```

---

## 🚀 Hướng dẫn cài đặt & Khởi chạy

### 1. Chuẩn bị môi trường
Tạo và kích hoạt virtual environment:
```bash
python -m venv .venv
# Trên Windows:
.venv\Scripts\activate
# Trên Linux/macOS:
source .venv/bin/activate
```

Cài đặt các gói thư viện:
```bash
pip install -r requirements.txt
```

### 2. Cấu hình biến môi trường
Sao chép `.env.example` thành `.env` và điền Google Gemini API Key:
```bash
cp .env.example .env
```
Cập nhật `GOOGLE_API_KEY` (lấy miễn phí từ [Google AI Studio](https://aistudio.google.com/)) và cấu hình Database trong `.env`.

### 3. Khởi động PostgreSQL + PGVector bằng Docker
```bash
docker compose up -d
```

### 4. Khởi chạy ứng dụng FastAPI
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## 📌 Kiểm thử API (Swagger UI)
Truy cập giao diện tương tác: [http://localhost:8000/docs](http://localhost:8000/docs)

1. **Upload tài liệu**:
   - `POST /api/v1/documents/upload`
   - Upload file PDF, TXT hoặc Markdown. Hệ thống sẽ tự động bóc tách, cắt chunk và lưu vector vào PGVector.

2. **Hỏi đáp tài liệu (RAG)**:
   - `POST /api/v1/chat/query`
   - Body mẫu:
     ```json
     {
       "query": "Nội dung chính của tài liệu là gì?",
       "k": 4
     }
     ```
