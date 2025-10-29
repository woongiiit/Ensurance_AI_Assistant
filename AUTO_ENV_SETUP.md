# Railway 환경 변수 자동 설정 가이드

Railway에서 환경 변수를 자동으로 설정하는 방법입니다.

## 자동 설정되는 환경 변수

### 백엔드 (`backend/railway.toml`)

```toml
[variables]
ADMIN_USERNAME = "admin"  # 자동 설정됨
```

### 프론트엔드 (`frontend/railway.toml`)

환경 변수는 `railway.toml`에서 정의하거나 Railway Variables에서 설정합니다.

## 수동 설정이 필요한 환경 변수

Railway Variables에서 직접 설정해야 하는 환경 변수:

### 백엔드 서비스

1. **DATABASE_URL** (자동)
   - PostgreSQL 서비스를 프로젝트에 연결하면 자동으로 설정됨
   - Railway의 서비스 참조 기능 사용

2. **SECRET_KEY** (수동)
   - Railway Variables에서 설정
   - 생성: `openssl rand -hex 32`

3. **GEMINI_API_KEY** (수동)
   - Railway Variables에서 설정

4. **ADMIN_PASSWORD** (수동)
   - Railway Variables에서 설정 (강력한 비밀번호 필수)

5. **FRONTEND_URL** (수동, 프론트엔드 배포 후)
   - 프론트엔드 서비스 URL

### 프론트엔드 서비스

1. **NEXT_PUBLIC_API_URL** (수동, 백엔드 배포 후)
   - 백엔드 서비스 URL

## Railway 서비스 참조를 이용한 자동 설정

Railway는 서비스 간 환경 변수를 자동으로 참조할 수 있습니다.

### 방법 1: Railway Variables에서 서비스 참조

1. **백엔드 Variables**에서:
   - `DATABASE_URL` 선택
   - PostgreSQL 서비스 연결 시 자동으로 생성됨

2. **프론트엔드 Variables**에서:
   - `NEXT_PUBLIC_API_URL` = 백엔드 서비스 URL
   - 또는 Railway가 제공하는 서비스 참조 사용

### 방법 2: Railway CLI 사용 (고급)

```bash
# Railway CLI 설치
npm i -g @railway/cli

# 로그인
railway login

# 프로젝트 연결
railway link

# 환경 변수 설정
railway variables set SECRET_KEY="your-secret-key" --service backend
railway variables set GEMINI_API_KEY="your-api-key" --service backend
railway variables set FRONTEND_URL="https://your-frontend.railway.app" --service backend

railway variables set NEXT_PUBLIC_API_URL="https://your-backend.railway.app" --service frontend
```

## 자동 설정 시나리오

### 1단계: PostgreSQL 서비스 추가
- `DATABASE_URL` 자동 생성

### 2단계: 백엔드 서비스 추가
- Root Directory: `backend`
- Railway Variables에서:
  - `SECRET_KEY` 설정
  - `GEMINI_API_KEY` 설정
  - `ADMIN_PASSWORD` 설정

### 3단계: 프론트엔드 서비스 추가
- Root Directory: `frontend`
- Railway Variables에서:
  - `NEXT_PUBLIC_API_URL` = 백엔드 URL 설정

### 4단계: 연결 설정
- 백엔드 Variables에서:
  - `FRONTEND_URL` = 프론트엔드 URL 설정

## 완전 자동화는 불가능한 이유

다음 환경 변수들은 보안상 수동 설정이 필수입니다:
- `SECRET_KEY`: 프로젝트마다 고유해야 함
- `GEMINI_API_KEY`: 외부 서비스 API 키
- `ADMIN_PASSWORD`: 관리자 비밀번호

이런 민감한 정보는 코드나 설정 파일에 포함하면 안 됩니다.

## 환경 변수 템플릿

Railway Variables에서 설정할 때 다음 템플릿을 참고하세요:

### 백엔드 템플릿
```
SECRET_KEY=<32자 이상 랜덤 문자열>
GEMINI_API_KEY=<Google Gemini API 키>
ADMIN_USERNAME minecraft
ADMIN_PASSWORD=<강력한 비밀번호>
FRONTEND_URL=https://your-frontend.railway.app
```

### 프론트엔드 템플릿
```
NEXT_PUBLIC_API_URL=https://your-backend.railway.app
```

