from app.security.verify_api_key import verify_api_key
from fastapi import Depends
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import init_db
from app.services.vector_store import init_vector_store
from app.api.v1.router import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: ensure pgvector extension and vector table exist
    try:
        init_db()
        init_vector_store()
        print("PGVector database and tables initialized successfully.")
    except Exception as e:
        print(f"Warning during DB/PGVector initialization: {e}")
    yield
    # Shutdown logic if needed


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API v1 router
app.include_router(
    api_router,
    prefix=settings.API_V1_STR,
    dependencies=[
        Depends(verify_api_key)
    ]
)


@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok", "app": settings.PROJECT_NAME}
