# Railway 배포 가이드 - 한국어

## 📍 백엔드 서비스 URL 확인 방법

### 1. Railway 대시보드에서 확인

1. **Railway 웹사이트 로그인** → https://railway.app
2. **프로젝트 선택**
3. **백엔드 서비스 선택** (첫 번째 서비스)
4. **상단에 표시된 URL 확인**
   - 예: `https://your-service.railway.app`
   - 또는 Settings → Domains에서 확인 가능

### 2. 터미널에서 확인 (Railway CLI 사용 시)

```bash
# Railway CLI 설치 (없다면)
npm i -g @railway/cli

# 로그인
railway login

# 프로젝트 연결
railway link

# 모든 서비스 URL 확인
railway status
```

## 🚀 배포 단계

### 1단계: PostgreSQL 데이터베이스 추가

1. Railway 대시보드 → **New** 클릭
2. **Database** → **Add PostgreSQL** 선택
3. 생성된 PostgreSQL 서비스 → **Variables** 탭
4. `DATABASE_URL` 값 복사
   - 형식: `postgresql://postgres:password@containers-us-xxx.railway.app:5432/railway`

### 2단계: 백엔드 배포

1. **New** → **GitHub Repo** 선택
2. **Ensurance_AI_Assistant** 레포지토리 선택
3. ⚠️ **중요: Settings에서 Root Directory 설정**
   - **Settings** 탭 클릭
   - **Root Directory**: `backend` 입력 후 저장
   - 이 설정을 하지 않으면 "Dockerfile does not exist" 오류 발생!
4. **Deploy** 시작 (자동으로 Dockerfile 감지)

#### 환경 변수 설정 (Variables 탭)
```
DATABASE_URL=postgresql://...(PostgreSQL에서 자동 제공)
SECRET_KEY=your-random-secret-key-here
GEMINI_API_KEY=your-google-gemini-api-key
ADMIN_USERNAME=admin
ADMIN_PASSWORD=your-secure-password
FRONTEND_URL=https://your-frontend.railway.app (나중에 설정)
```

### 3단계: 프론트엔드 배포

1. **New** → **GitHub Repo** 선택
2. **Ensurance_AI_Assistant** 레포지토리 선택 (동일한 레포)
3. ⚠️ **중요: Settings에서 Root Directory 설정**
   - **Settings** 탭 클릭
   - **Root Directory**: `frontend` 입력 후 저장
   - 이 설정을 하지 않으면 "Dockerfile does not exist" 오류 발생!
4. **Deploy** 시작

#### 환경 변수 설정 (Variables 탭)
```
NEXT_PUBLIC_API_URL=https://your-backend.railway.app
```

### 4단계: 서비스 URL 확인 및 연결

#### 백엔드 URL 확인
- **백엔드 서비스 페이지** → 상단에서 URL 복사
- 예: `https://your-backend.railway.app`

#### 프론트엔드 URL 확인
- **프론트엔드 서비스 페이지** → 상단에서 URL 복사
- 예: `https://your-frontend.railway.app`

#### 서로 연결
1. **백엔드 서비스** → **Variables** → `FRONTEND_URL` 설정
   - 값: 프론트엔드 URL 입력
2. **프론트엔드 서비스** → **Variables** → `NEXT_PUBLIC_API_URL` 설정
   - 값: 백엔드 URL 입력

### 5단계: PostgreSQL 확장 설치

1. Railway 대시보드 → **PostgreSQL 서비스** 선택
2. **Data** 탭 클릭
3. **Connect** 버튼 → **Query** 선택
4. 다음 SQL 실행:

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

### 6단계: 관리자 계정 초기화

터미널에서 (PowerShell):
```powershell
Invoke-RestMethod -Uri "https://your-backend.railway.app/api/v1/auth/init-admin" -Method POST
```

또는:
```bash
curl -X POST "https://your-backend.railway.app/api/v1/auth/init-admin"
```

## 📝 서비스 URL 위치 요약

| 항목 | 확인 위치 |
|------|----------|
| **백엔드 URL** | 백엔드 서비스 페이지 상단 |
| **프론트엔드 URL** | 프론트엔드 서비스 페이지 상단 |
| **DATABASE_URL** | PostgreSQL 서비스 → Variables 탭 |

## 🔧 문제 해결

### ❌ "Dockerfile does not exist" 오류

**원인**: Root Directory가 설정되지 않음

**해결 방법**:
1. Railway 대시보드 → 해당 서비스 선택
2. **Settings** 탭 클릭
3. **Root Directory** 필드에 다음 입력:
   - 백엔드: `backend`
   - 프론트엔드: `frontend`
4. **Save** 클릭
5. **Deploy** 다시 실행

### 서비스가 시작되지 않을 때
- 서비스 → **Logs** 탭에서 오류 확인
- **Variables** 탭에서 환경 변수 확인

### CORS 오류가 발생할 때
- 백엔드 `FRONTEND_URL` 환경 변수가 정확한지 확인
- 프론트엔드 URL과 백엔드에 설정한 URL이 일치하는지 확인

### 데이터베이스 연결 오류
- PostgreSQL 서비스가 실행 중인지 확인
- `DATABASE_URL` 환경 변수가 올바른지 확인

## ✅ 배포 확인

1. **백엔드 헬스 체크**
   - 브라우저: `https://your-backend.railway.app/health`
   - 응답: `{"status": "healthy"}`

2. **프론트엔드 접속**
   - 브라우저: 프론트엔드 URL 열기
   - 채팅 기능 테스트

3. **관리자 페이지 접속**
   - 프론트엔드 URL + `/admin/login`
   - 관리자 계정으로 로그인 테스트

