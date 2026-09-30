
# Document AI & RAG Service - Python API

Dịch vụ AI Backend chuyên trách trích xuất nội dung tài liệu, lập chỉ mục vector và thực hiện truy xuất tri thức theo cơ chế RAG (Retrieval-Augmented Generation), phục vụ chức năng hỏi đáp thông minh theo từng dự án.



## Công nghệ sử dụng

- **Nền tảng:** Python 3.11+, FastAPI, Uvicorn
- **Xử lý AI:** LangChain, `langchain-core`, `langchain-community`, `langchain-google-genai`
- **Mô hình ngôn ngữ và tạo vector:** Google Gemini
- **Cơ sở dữ liệu vector:** PostgreSQL, PGVector, `langchain-postgres`, SQLAlchemy, `psycopg3`
- **Xử lý tài liệu:** PyPDF, `python-docx`, bộ phân tích Markdown/Text, `RecursiveCharacterTextSplitter`
- **Lưu trữ đối tượng:** MinIO Python Client


## Tính năng chính

1. **Trích xuất nội dung tài liệu**
   - Đọc trực tiếp tệp từ MinIO theo `project_id` và `object_name`.
   - Hỗ trợ các định dạng:
     - PDF
     - DOCX
     - Markdown (`.md`)
     - Text (`.txt`)

2. **Chia đoạn và tạo vector**
   - Tự động chia nội dung thành các đoạn văn bản phù hợp.
   - Sử dụng cơ chế chồng lấn giữa các đoạn để duy trì ngữ cảnh.
   - Tạo vector biểu diễn cho từng đoạn văn bản.
   - Lưu vector vào PGVector cùng metadata:
     - `project_id`
     - `source`
     - `page_number`

3. **Hỏi đáp dựa trên ngữ cảnh**
   - Tìm kiếm các đoạn tài liệu phù hợp bằng độ tương đồng vector.
   - Giới hạn phạm vi truy xuất theo danh sách tài liệu được người dùng lựa chọn.
   - Sinh câu trả lời dựa trên nội dung tài liệu được truy xuất.
   - Trả về thông tin nguồn tài liệu được sử dụng trong câu trả lời.



## Khởi chạy dịch vụ

### 1. Tạo môi trường ảo và cài đặt thư viện

```bash
python -m venv .venv
````

**Windows:**

```bash
.venv\Scripts\activate
```

**Linux/macOS:**

```bash
source .venv/bin/activate
```

Cài đặt các thư viện:

```bash
pip install -r requirements.txt
```

### 2. Cấu hình biến môi trường

Tạo file `.env` tại thư mục gốc:

```env
GOOGLE_API_KEY=your_google_gemini_api_key

POSTGRES_DB=document_management_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
MINIO_BUCKET_NAME=document-management
```

### 3. Khởi chạy dịch vụ FastAPI

```bash
fastapi dev app/main.py --port 8000
```

Sau khi khởi chạy thành công:

* **API Server:** `http://localhost:8000`
* **Swagger UI:** `http://localhost:8000/docs`
* **OpenAPI JSON:** `http://localhost:8000/openapi.json`


