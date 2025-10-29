from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import Generator
import google.generativeai as genai
import json
import uuid
from datetime import datetime

from core.config import settings
from core.database import get_db, get_vector_db
from models.database import ChatMessage, DocumentChunk
from schemas.api import ChatRequest
from core.auth import get_current_admin

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


def search_similar_chunks(query: str, db: Session, limit: int = 5) -> list:
    """Search for similar chunks using simple text search"""
    try:
        # Simple text search for development
        chunks = db.query(DocumentChunk).filter(
            DocumentChunk.content.contains(query)
        ).limit(limit).all()
        
        # If no chunks found, return any chunks
        if not chunks:
            chunks = db.query(DocumentChunk).limit(limit).all()
        
        return chunks
    except Exception as e:
        print(f"Error searching chunks: {e}")
        return []


def generate_chat_response(query: str, context_chunks: list) -> Generator[str, None, None]:
    """Generate streaming response from Gemini"""
    try:
        # Prepare context from chunks
        context = "\n".join([chunk.content[:500] for chunk in context_chunks[:3]])  # Limit context length
        
        # Create prompt
        prompt = f"""
        다음은 보험 약관 관련 문서의 일부입니다:
        
        {context}
        
        사용자 질문: {query}
        
        위 문서 내용을 바탕으로 정확하고 도움이 되는 답변을 제공해주세요. 
        문서에 없는 내용은 추측하지 말고, 문서 내용만을 바탕으로 답변해주세요.
        """
        
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt, stream=True)
        
        for chunk in response:
            if chunk.text:
                yield f"data: {json.dumps({'content': chunk.text})}\n\n"
        
        yield "data: [DONE]\n\n"
    except Exception as e:
        print(f"Error generating response: {e}")
        yield f"data: {json.dumps({'content': '죄송합니다. 답변을 생성하는 중 오류가 발생했습니다.'})}\n\n"
        yield "data: [DONE]\n\n"


@router.post("/chat")
async def chat(request: ChatRequest, db: Session = Depends(get_db), vector_db: Session = Depends(get_vector_db)):
    """Chat endpoint with RAG"""
    try:
        # Generate session ID
        session_id = str(uuid.uuid4())
        
        # Search for similar chunks
        similar_chunks = search_similar_chunks(request.message, vector_db)
        
        # Save user message
        user_message = ChatMessage(
            session_id=session_id,
            role="user",
            content=request.message
        )
        db.add(user_message)
        db.commit()
        
        # Generate streaming response
        def response_generator():
            full_response = ""
            for chunk in generate_chat_response(request.message, similar_chunks):
                if chunk.startswith("data: ") and not chunk.startswith("data: [DONE]"):
                    try:
                        data = json.loads(chunk[6:])
                        full_response += data['content']
                    except:
                        pass
                yield chunk
            
            # Save AI response
            ai_message = ChatMessage(
                session_id=session_id,
                role="ai",
                content=full_response
            )
            db.add(ai_message)
            db.commit()
        
        return StreamingResponse(
            response_generator(),
            media_type="text/plain",
            headers={"Cache-Control": "no-cache", "Connection": "keep-alive"}
        )
        
    except Exception as e:
        print(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
