from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


# Chat schemas
class ChatRequest(BaseModel):
    message: str


class ChatMessageResponse(BaseModel):
    id: int
    session_id: str
    role: str
    content: str
    created_at: datetime
    
    class Config:
        from_attributes = True


# Auth schemas
class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


# Admin schemas
class DocumentUploadResponse(BaseModel):
    message: str
    document_id: int


class DocumentResponse(BaseModel):
    id: int
    file_name: str
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class DocumentListResponse(BaseModel):
    documents: List[DocumentResponse]
    total: int
    page: int
    size: int


class ChatHistoryResponse(BaseModel):
    messages: List[ChatMessageResponse]
    total: int
    page: int
    size: int

