# 보험 약관 PDF 기반 RAG AI 챗봇 웹 서비스

이 프로젝트는 보험 약관 PDF 문서를 기반으로 한 RAG(Retrieval-Augmented Generation) AI 챗봇 웹 서비스입니다.

## 기술 스택

- **백엔드**: Python, FastAPI
- **프론트엔드**: Next.js (TypeScript)
- **LLM**: Google Gemini API
- **데이터베이스**: PostgreSQL + pgvector
- **배포**: Railway

## 프로젝트 구조

```
├── backend/                 # FastAPI 백엔드
│   ├── api/v1/             # API 라우터
│   ├── core/               # 핵심 설정
│   ├── models/             # SQLAlchemy 모델
│   ├── schemas/             # Pydantic 스키마
│   ├── main.py             # FastAPI 앱 진입점
│   └── requirements.txt     # Python 의존성
├── frontend/               # Next.js 프론트엔드
│   ├── src/app/            # Next.js 앱 라우터
│   ├── src/app/admin/      # 관리자 페이지
│   └── package.json        # Node.js 의존성
└── README.md
```

## 설치 및 실행

### 1. 데이터베이스 설정

PostgreSQL 데이터베이스에 pgvector 확장을 설치합니다:

```sql
CREATE EXTENSION vector;
```

### 2. 백엔드 설정

```bash
cd backend
pip install -r requirements.txt
```

환경 변수 설정:
```bash
cp env.example .env
# .env 파일을 편집하여 실제 값으로 변경
```

백엔드 실행:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 3. 프론트엔드 설정

```bash
cd frontend
npm install
```

환경 변수 설정:
```bash
cp env.local.example .env.local
# .env.local 파일을 편집하여 Gemini API 키 설정
```

프론트엔드 실행:
```bash
npm run dev
```

### 4. 관리자 계정 초기화

백엔드가 실행된 상태에서 다음 API를 호출하여 관리자 계정을 생성합니다:

```bash
curl -X POST "http://localhost:8000/api/v1/auth/init-admin"
```

## 주요 기능

### 일반 사용자 기능
- **채팅 인터페이스**: 보험 약관에 대해 질문할 수 있는 ChatGPT 스타일의 UI
- **RAG 기반 답변**: 업로드된 PDF 문서를 기반으로 정확한 답변 제공

### 관리자 기능
- **로그인**: JWT 기반 인증
- **채팅 내역 조회**: 모든 사용자 채팅 내역 확인
- **문서 관리**: PDF 문서 업로드, 목록 조회, 삭제
- **RAG 인덱싱**: PDF 텍스트 추출, 청킹, 임베딩 생성

## API 엔드포인트

### 채팅 API
- `POST /api/v1/chat` - 채팅 메시지 전송 (스트리밍 응답)

### 인증 API
- `POST /api/v1/auth/login` - 관리자 로그인
- `POST /api/v1/auth/init-admin` - 관리자 계정 초기화

### 관리자 API (인증 필요)
- `GET /api/v1/admin/chat-history` - 채팅 내역 조회
- `POST /api/v1/admin/documents/upload` - 문서 업로드
- `GET /api/v1/admin/documents` - 문서 목록 조회
- `DELETE /api/v1/admin/documents/{doc_id}` - 문서 삭제

## 데이터베이스 스키마

### 일반 테이블
- `admin_users`: 관리자 계정 정보
- `chat_messages`: 채팅 메시지 내역
- `indexed_documents`: 인덱싱된 문서 메타데이터

### 벡터 테이블
- `document_chunks`: 문서 청크와 임베딩 벡터

## 환경 변수

### 백엔드 (.env)
```
DATABASE_URL=postgresql://username:password@localhost:5432/insurance_rag_db
VECTOR_DATABASE_URL=postgresql://username:password@localhost:5432/insurance_rag_db
SECRET_KEY=your-secret-key-here
GEMINI_API_KEY=your-gemini-api-key-here
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123
FRONTEND_URL=http://localhost:3000
```

### 프론트엔드 (.env.local)
```
GOOGLE_GENERATIVE_AI_API_KEY=your-gemini-api-key-here
```

## 배포

### Railway 배포
1. GitHub 저장소에 코드 푸시
2. Railway에서 새 프로젝트 생성
3. PostgreSQL 데이터베이스 추가
4. 환경 변수 설정
5. 배포 완료

## 개발 가이드

### 새로운 기능 추가
1. 백엔드: `api/v1/` 디렉토리에 새 라우터 추가
2. 프론트엔드: `src/app/` 디렉토리에 새 페이지 추가
3. API 통신: fetch 또는 axios 사용

### 데이터베이스 마이그레이션
SQLAlchemy 모델 변경 시 데이터베이스 스키마를 수동으로 업데이트해야 합니다.

## 문제 해결

### 일반적인 문제
1. **CORS 오류**: 백엔드 CORS 설정 확인
2. **인증 오류**: JWT 토큰 만료 확인
3. **벡터 검색 오류**: pgvector 확장 설치 확인
4. **PDF 업로드 오류**: 파일 크기 및 형식 확인

### 로그 확인
- 백엔드: 터미널 출력 확인
- 프론트엔드: 브라우저 개발자 도구 콘솔 확인

