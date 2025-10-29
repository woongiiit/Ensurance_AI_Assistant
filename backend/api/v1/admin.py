from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query
from sqlalchemy.orm import Session
from typing import List
import PyPDF2
import io
import google.generativeai as genai
from datetime import datetime

from core.config import settings
from core.database import get_db, get_vector_db
from core.auth import get_current_admin
from models.database import AdminUser, ChatMessage, IndexedDocument, DocumentChunk
from schemas.api import (
    DocumentUploadResponse, 
    DocumentResponse, 
    DocumentListResponse,
    ChatHistoryResponse,
    ChatMessageResponse
)

router = APIRouter()

# Configure Gemini API
genai.configure(api_key=settings.gemini_api_key)


def get_embeddings(text: str) -> list:
    """Get embeddings from Gemini API"""
    try:
        model = genai.GenerativeModel('embedding-001')
        result = model.embed_content(text)
        return result['embedding']
    except Exception as e:
        print(f"Error getting embeddings: {e}")
        return []


def extract_text_from_pdf(file_content: bytes) -> str:
    """Extract text from PDF file"""
    pdf_file = io.BytesIO(file_content)
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    
    return text


def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
    """Split text into chunks with overlap"""
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap
    
    return chunks


@router.get("/chat-history", response_model=ChatHistoryResponse)
async def get_chat_history(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    current_admin: AdminUser = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get chat history with pagination"""
    offset = (page - 1) * size
    
    messages = db.query(ChatMessage).order_by(ChatMessage.created_at.desc()).offset(offset).limit(size).all()
    total = db.query(ChatMessage).count()
    
    return ChatHistoryResponse(
        messages=messages,
        total=total,
        page=page,
        size=size
    )


@router.post("/documents/upload", response_model=DocumentUploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    current_admin: AdminUser = Depends(get_current_admin),
    db: Session = Depends(get_db),
    vector_db: Session = Depends(get_vector_db)
):
    """Upload and index PDF document"""
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    try:
        # Read file content
        file_content = await file.read()
        
        # Create document record
        document = IndexedDocument(
            file_name=file.filename,
            status='indexing'
        )
        db.add(document)
        db.commit()
        db.refresh(document)
        
        try:
            # Extract text from PDF
            text = extract_text_from_pdf(file_content)
            
            # Chunk the text
            chunks = chunk_text(text)
            
            # Process each chunk
            for chunk_text in chunks:
                # Get embedding
                embedding = get_embeddings(chunk_text)
                
                # Create chunk record
                chunk = DocumentChunk(
                    document_id=document.id,
                    content=chunk_text,
                    embedding=str(embedding)  # Store as string for now
                )
                vector_db.add(chunk)
            
            vector_db.commit()
            
            # Update document status
            document.status = 'ready'
            db.commit()
            
            return DocumentUploadResponse(
                message="Document uploaded and indexed successfully",
                document_id=document.id
            )
            
        except Exception as e:
            # Update document status to error
            document.status = 'error'
            db.commit()
            raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading document: {str(e)}")


@router.get("/documents", response_model=DocumentListResponse)
async def get_documents(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    current_admin: AdminUser = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get list of indexed documents"""
    offset = (page - 1) * size
    
    documents = db.query(IndexedDocument).order_by(IndexedDocument.created_at.desc()).offset(offset).limit(size).all()
    total = db.query(IndexedDocument).count()
    
    return DocumentListResponse(
        documents=documents,
        total=total,
        page=page,
        size=size
    )


@router.delete("/documents/{doc_id}")
async def delete_document(
    doc_id: int,
    current_admin: AdminUser = Depends(get_current_admin),
    db: Session = Depends(get_db),
    vector_db: Session = Depends(get_vector_db)
):
    """Delete document and its chunks"""
    # Find document
    document = db.query(IndexedDocument).filter(IndexedDocument.id == doc_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    try:
        # Delete chunks from vector database
        vector_db.query(DocumentChunk).filter(DocumentChunk.document_id == doc_id).delete()
        vector_db.commit()
        
        # Delete document
        db.delete(document)
        db.commit()
        
        return {"message": "Document deleted successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting document: {str(e)}")
