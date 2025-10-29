from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from core.config import settings

# PostgreSQL 연결을 위해 URL 변환 (Railway는 postgres:// 형식을 사용)
database_url = settings.database_url.replace("postgres://", "postgresql://")
vector_database_url = settings.vector_database_url.replace("postgres://", "postgresql://")

# Create database engine
engine = create_engine(database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create vector database engine for pgvector
vector_engine = create_engine(vector_database_url, pool_pre_ping=True)
VectorSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=vector_engine)

Base = declarative_base()


def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_vector_db():
    """Dependency to get vector database session"""
    db = VectorSessionLocal()
    try:
        yield db
    finally:
        db.close()

