# 백엔드 환경 변수 체크리스트

Railway 백엔드 서비스에서 설정해야 할 환경 변수와 점검 사항입니다.

## ✅ 필수 환경 변수

### 1. DATABASE_URL
- **설정 방법**: Railway가 PostgreSQL 서비스 추가 시 자동으로 제공
- **형식**: `postgresql://postgres:password@containers-us-xxx.railway.app:5432/railway`
- **확인 사항**:
  - ✅ `postgresql://` 또는 `postgres://`로 시작해야 함
  - ✅ Railway의 PostgreSQL 서비스 → Variables 탭에서 복사
  - ✅ 수동으로 입력하지 말고 Railway가 제공하는 값 사용

### 2. SECRET_KEY
- **목적**: JWT 토큰 서명에 사용
- **설정 방법**: Railway Variables 탭에서 직접 입력
- **확인 사항**:
  - ✅ 최소 32자 이상의 랜덤 문자열
  - ❌ `your-secret-key-here` 같은 기본값 사용 금지
  - ❌ 예측 가능한 값 사용 금지
- **생성 방법** (터미널):
  ```bash
  openssl rand -hex 32
  ```
  또는 Python:
  ```python
  import secrets
  print(secrets.token_hex(32))
  ```

### 3. GEMINI_API_KEY
- **목적**: Google Gemini API 접근
- **설정 방법**: Google AI Studio 또는 Google Cloud Console에서 발급
- **확인 사항**:
  - ✅ 유효한 API 키가 입력되어 있어야 함
  - ❌ `your-gemini-api-key-here` 같은 기본값 사용 금지
  - ✅ API 키는 비공개로 유지

### 4. FRONTEND_URL
- **목적**: CORS 설정용 프론트엔드 URL
- **설정 방법**: 프론트엔드 배포 후 받은 URL 입력
- **확인 사항**:
  - ✅ `https://` 또는 `http://`로 시작
  - ✅ 프론트엔드 서비스의 실제 URL과 정확히 일치
  - ✅ 예: `https://your-frontend-production.up.railway.app`
  - ❌ `http://localhost:3000` 같은 로컬 URL 사용 금지

## ⚠️ 선택적 환경 변수 (권장)

### 5. ADMIN_USERNAME
- **기본값**: `admin`
- **확인 사항**:
  - ✅ 기본값 사용 가능하지만, 보안을 위해 변경 권장

### 6. ADMIN_PASSWORD
- **기본값**: `admin123`
- **확인 사항**:
  - ❌ **절대 기본값(`admin123`) 사용 금지!**
  - ✅ 최소 8자 이상, 영문 대소문자, 숫자, 특수문자 포함
  - ✅ 강력한 비밀번호 사용 필수

### 7. VECTOR_DATABASE_URL (선택)
- **목적**: 벡터 검색용 별도 데이터베이스 (없으면 DATABASE_URL 사용)
- **설정 방법**: 별도 PostgreSQL 서비스가 있으면 설정

## 🔍 빠른 점검 체크리스트

Railway 백엔드 서비스 → **Variables** 탭에서 확인:

- [ ] `DATABASE_URL`: Railway PostgreSQL에서 자동 제공됨
- [ ] `SECRET_KEY`: 32자 이상의 랜덤 문자열
- [ ] `GEMINI_API_KEY`: 실제 Google Gemini API 키
- [ ] `FRONTEND_URL`: 실제 프론트엔드 배포 URL (https://로 시작)
- [ ] `ADMIN_USERNAME`: 기본값 또는 커스텀 값
- [ ] `ADMIN_PASSWORD`: 기본값(`admin123`)이 아닌 강력한 비밀번호

## ❌ 흔한 실수

1. **SECRET_KEY에 기본값 사용**
   - ❌ `your-secret-key-here`
   - ✅ `a1b2c3d4e5f6...` (32자 이상 랜덤)

2. **ADMIN_PASSWORD에 기본값 사용**
   - ❌ `admin123`
   - ✅ 강력한 비밀번호

3. **FRONTEND_URL에 로컬 주소 사용**
   - ❌ `http://localhost:3000`
   - ✅ `https://your-frontend.railway.app`

4. **GEMINI_API_KEY 미입력 또는 기본값**
   - ❌ `your-gemini-api-key-here`
   - ✅ 실제 API 키

## 🚀 설정 순서

1. PostgreSQL 서비스 생성 → `DATABASE_URL` 자동 생성
2. `SECRET_KEY` 생성 후 입력
3. `GEMINI_API_KEY` 입력
4. 프론트엔드 배포 후 URL 확인
5. `FRONTEND_URL`에 프론트엔드 URL 입력
6. `ADMIN_PASSWORD` 설정 (강력한 비밀번호)
7. 재배포

