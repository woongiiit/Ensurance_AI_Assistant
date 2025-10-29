# Railway 배포 문제 해결 가이드

## 백엔드 "service unavailable" 오류 해결

### 문제 증상
```
Attempt #1 failed with service unavailable. Continuing to retry for 1m36s
Attempt #2 failed with service unavailable. Continuing to retry for 1m35s
```

### 가능한 원인 및 해결 방법

#### 1. 애플리케이션이 시작되지 않음

**확인训练:**
- Railway 대시보드 → 백엔드 서비스 → **Logs** 탭 확인
- 오류 메시지 확인

**해결 방법:**
```bash
# 로컬에서 테스트
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000
```

#### 2. 데이터베이스 연결 실패

**확인 사항:**
- `DATABASE_URL` 환경 변수가 올바른지 확인
- PostgreSQL 서비스가 실행 중인지 확인
- Railway Variables에서 `DATABASE_URL` 확인

**해결 방법:**
1. Railway 대시보드 → PostgreSQL 서비스 → **Variables** 탭
2. `DATABASE_URL` 값 확인
3. 백엔드 서비스 → **Variables** 탭
4. `DATABASE_URL`이 올바르게 설정되어 있는지 확인

#### 3. Health Check 타이밍 문제

**확인 사항:**
- 애플리케이션이 시작되는 데 시간이 걸리는 경우
- Health check가 너무 빨리 실행되는 경우

**해결 방법:**
- `railway.toml`의 `healthcheckTimeout`을 증가시킴 (300초)
- 이미 적용됨 ✅

#### 4. 포트 바인딩 문제

**확인 사항:**
- Railway Settings → Networking → Port 설정
- `$PORT` 환경 변수가 올바르게 설정되었는지

**해결 방법:**
1. Railway Settings → Networking
2. Port 설정 확인 (예: 8080)
3. `railway.toml`의 `startCommand`에서 `$PORT` 사용 확인

#### 5. 환경 변수 누락

**확인 사항:**
필수 환경 변수:
- `DATABASE_URL` ✅
- `SECRET_KEY` ✅
- `GEMINI_API_KEY` ✅
- `ADMIN_PASSWORD` ✅
- `FRONTEND_URL` (선택, 프론트엔드 배포 후)

**해결 방법:**
1. Railway Variables에서 모든 필수 환경 변수 확인
2. 누락된 변수 추가

### 디버깅 단계

1. **Logs 확인**
   - Railway 대시보드 → 백엔드 서비스 → **Logs** 탭
   - 실제 오류 메시지 확인

2. **환경 변수 확인**
   - Railway Variables에서 모든 변수 확인
   - 특히 `DATABASE_URL`, `SECRET_KEY` 확인

3. **Health Check 수동 테스트**
   배포 후:
   ```bash
   curl https://your-backend.railway.app/health
   ```
   또는 PowerShell:
   ```powershell
   Invoke-RestMethod -Uri "https://your-backend.railway.app/health"
   ```

4. **로컬 테스트**
   ```bash
   cd backend
   # 환경 변수 설정
   export DATABASE_URL="your-database-url"
   export SECRET_KEY="your-secret-key"
   export GEMINI_API_KEY="your-api-key"
   
   # 실행
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

### 일반적인 오류 메시지

| 오류 메시지 | 원인 | 해결 방법 |
|------------|------|----------|
| `connection refused` | 데이터베이스 연결 실패 | `DATABASE_URL` 확인 |
| `invalid secret key` | SECRET_KEY 누락 | Railway Variables에서 설정 |
| `module not found` | 의존성 누락 | `requirements.txt` 확인 |
| `port already in use` | 포트 충돌 | Railway가 자동 관리하므로 문제 없음 |

### 추가 확인 사항

1. **빌드 로그 확인**
   - Railway Deployments → 최신 배포 → Build Logs
   - 빌드 오류 확인

2. **실행 로그 확인**
   - Railway Deployments → 최신 배포 → Runtime Logs
   - 실행 오류 확인

3. **서비스 상태**
   - Railway 서비스가 "Active" 상태인지 확인
   - 재시작이 반복되지 않는지 확인

