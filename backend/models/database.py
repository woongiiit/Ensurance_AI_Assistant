from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from core.database import Base


class AdminUser(Base):
    __tablename__ = "admin_users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)


class ChatMessage(Base):
    __tablename__ = "chat_messages"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(255), index=True, nullable=False)
    role = Column(String(10), nullable=False)  # 'user' or 'ai'
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    __table_args__ = (
        Index('idx_session_role', 'session_id', 'role'),
    )


class IndexedDocument(Base):
    __tablename__ = "indexed_documents"
    
    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String(255), nullable=False)
    status = Column(String(20), nullable=False, default='indexing')  # 'indexing', 'ready', 'error'
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationship to document chunks
    chunks = relationship("DocumentChunk", back_populates="document", cascade="all, delete-orphan")


class DocumentChunk(Base):
    __tablename__ = "document_chunks"
    
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("indexed_documents.id"), nullable=False, index=True)
    content = Column(Text, nullable=False)
    embedding = Column(String, nullable=False)  # Will store vector as string for pgvector
    
    # Relationship to parent document
    document = relationship("IndexedDocument", back_populates="chunks")
    
    __table_args__ = (
        Index('idx_document_id', 'document_id'),
    )

