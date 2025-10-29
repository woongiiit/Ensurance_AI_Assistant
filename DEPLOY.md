# Railway 배포 가이드

이 문서는 Ensurance AI Assistant를 Railway에 배포하는 방법을 설명합니다.

## 1. Railway 프로젝트 생성

1. [Railway](https://railway.app)에 로그인
2. "New Project" 클릭
3. GitHub 레포지토리 연결

## 2. PostgreSQL 데이터베이스 추가

1. 프로젝트에서 "New" 버튼 클릭
2. "Database" → "Add PostgreSQL" 선택
3. 생성된 PostgreSQL 서비스의 Variables 탭에서 `DATABASE_URL` 복사

## 3. 백엔드 서비스 추가

1. 프로젝트에서 "New" 버튼 클릭
2. "GitHub Repo" 또는 "Empty Service" 선택
3. 레포지토리 연결 후 루트 디렉토리를 `backend`로 설정
4. 환경 변수 설정:
   - `DATABASE_URL`: PostgreSQL에서 제공하는 URL
   - `SECRET_KEY`: 랜덤 문자열 (e.g., `openssl rand -hex 32`)
   - `GEMINI_API_KEY`: Google Gemini API 키
   - `ADMIN_USERNAME`: 관리자 계정 이름
   - `ADMIN_PASSWORD`: 관리자 비밀번호 (강력한 비밀번호 사용)
   - `FRONTEND_URL`: 프론트엔드 URL (배포 후 설정)

## 4. 프론트엔드 서비스 추가

1. 프로젝트에서 "New" 버튼 클릭
2. 레포지토리 연결 후 루트 디렉토리를 `frontend`로 설정
3. 환경 변수 설정:
   - `NEXT_PUBLIC_API_URL`: 백엔드 서비스 URL

## 5. 배포 완료

배포가 완료되면:
1. 백엔드 서비스의 URL 복사
2. 프론트엔드 서비스의 URL 복사
3. 백엔드 환경 변수 `FRONTEND_URL`을 프론트엔드 URL로 설정
4. 프론트엔드 환경 변수 `NEXT_PUBLIC_API_URL`을 백엔드 URL로 설정
5. 재배포 실행

## 6. 관리자 계정 초기화

배포 후 다음 API를 호출하여 관리자 계정을 생성합니다:

```bash
curl -X POST "https://your-backend.railway.app/api/v1/auth/init-admin"
```

## 7. pgvector 확장 설치

Railway PostgreSQL 콘솔에서 다음 SQL 실행:

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

## 트러블슈팅

### 데이터베이스 연결 오류
- `DATABASE_URL` 환경 변수 확인
- PostgreSQL 서비스가 실행 중인지 확인

### CORS 오류
- 백엔드의 `FRONTEND_URL` 환경 변수가 정확한지 확인

### 빌드 실패
- Dockerfile 경로 확인
- 의존성 설치 오류 확인

