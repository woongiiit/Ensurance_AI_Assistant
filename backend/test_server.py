from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Insurance RAG Chatbot API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Insurance RAG Chatbot API - Test Server"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/api/v1/chat")
async def test_chat(request: dict):
    message = request.get("message", "")
    
    # 간단한 테스트 응답
    if "안녕" in message or "hello" in message.lower():
        return {"content": "안녕하세요! 보험 약관 AI 챗봇입니다. 무엇을 도와드릴까요?"}
    elif "보험" in message:
        return {"content": "보험에 대한 질문이군요. 현재는 테스트 모드입니다. 실제 보험 약관 문서가 업로드되면 더 정확한 답변을 제공할 수 있습니다."}
    else:
        return {"content": f"'{message}'에 대한 질문을 받았습니다. 현재는 테스트 모드입니다."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
