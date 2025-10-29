# Railway Port 설정 가이드

## 포트 설정 방법

### 1. Settings에서 설정 (권장)

Railway 대시보드에서:
1. 백엔드 서비스 선택
2. **Settings** 탭 클릭
3. **Networking** 섹션에서 **Port** 설정
4. 예: `8080` 입력

이렇게 설정하면:
- Railway가 `PORT` 환경 변수를 자동으로 설정 (예: `8080`)
- 애플리케이션은 `$PORT`를 통해 포트를 읽음
- **문제 없음** ✅

### 2. 환경 변수로 설정

Railway Variables에서:
- `PORT` = `8080` 설정

하지만 Settings에서 설정하는 게 더 권장됩니다.

## 현재 설정 상태

### 백엔드 설정 (`backend/railway.toml`)
```toml
startCommand = "uvicorn main:app --host 0.0.0.0 --port $PORT"
```

### 동작 방식
1. Railway Settings에서 Port = `8080` 설정
2. Railway가 `PORT` 환경 변수 = `8080` 설정
3. 애플리케이션 실행 시 `$PORT`가 `8080`으로 치환됨
4. 최종 명령어: `uvicorn main:app --host 0.0.0.0 --port 8080`
5. 정상 작동 ✅

## 이전 오류와 현재 상태

### 이전 오류 (이미 수정됨)
```
startCommand = "python -m uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"
Error: Invalid value for '--port': '${PORT:-8000}' is not a valid integer.
```
❌ **문제**: `${PORT:-8000}` 형식이 Railway에서 해석되지 않음

### 현재 설정 (수정됨)
```
startCommand = "uvicorn main:app --host 0.0.0.0 --port $PORT"
```
✅ **정상**: Railway가 `$PORT`를 정상적으로 치환

## 포트 설정 확인

### Settings에서 확인
- 백엔드 서비스 → Settings → Networking
- Port: `8080` (또는 사용자가 설정한 값)

### 환경 변수 확인
- Railway Variables에서 `PORT` 변수 확인
- Settings에서 설정하면 자동으로 생성됨

## 포트 변경 시

만약 포트를 다른 값으로 변경하려면:
1. Settings → Networking → Port 변경
2. 예: `3000`, `8000`, `9090` 등
3. 재배포 (자동으로 트리거됨)

## 권장 포트 값

- **백엔드**: `8000` (기본값), `8080`, `8001` 등
- **프론트엔드**: `3000` (기본값), `3001` 등

**중요**: Railway는 자동으로 사용 가능한 포트를 할당하므로, Settings에서 명시적으로 설정하지 않아도 됩니다. 하지만 명시적으로 설정하면 더 예측 가능합니다.

