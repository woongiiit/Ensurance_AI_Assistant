from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from core.config import settings
from core.database import engine, vector_engine
from models.database import Base
from api.v1 import chat, auth, admin


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    try:
        # Create tables
        Base.metadata.create_all(bind=engine)
        Base.metadata.create_all(bind=vector_engine)
        print("✅ Database tables created successfully")
    except Exception as e:
        print(f"⚠️  Warning: Database initialization error: {e}")
        # Continue anyway - tables might already exist
    yield
    # Shutdown
    pass


app = FastAPI(
    title="Insurance RAG Chatbot API",
    description="AI chatbot service for insurance policy documents",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat.router, prefix="/api/v1", tags=["chat"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(admin.router, prefix="/api/v1/admin", tags=["admin"])


@app.get("/")
async def root():
    return {"message": "Insurance RAG Chatbot API"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}

