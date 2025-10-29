# Railway 환경 변수: 유지 vs 삭제 가이드

## ✅ 절대 지우면 안 되는 환경 변수

### 백엔드 서비스 Variables에서 유지해야 할 항목:

1. **DATABASE_URL** ❌ 지우지 마세요!
   - PostgreSQL 서비스에서 자동 생성됨
   - Railway가 자동으로 관리
   
2. **SECRET_KEY** ❌ 지우지 마세요!
   - 보안상 필수
   - JWT 토큰 서명에 사용
   - 수동 설정 필요
   
3. **GEMINI_API_KEY** ❌ 지우지 마세요!
   - Google Gemini API 접근용
   - 수동 설정 필요
   
4. **ADMIN_PASSWORD** ❌ 지우지 마세요!
   - 관리자 비밀번호
   - 기본값(`admin123`) 사용 금지
   - 강력한 비밀번호 필요
   
5. **FRONTEND_URL** ❌ 지우지 마세요!
   - 프론트엔드 배포 후 설정
   - CORS 설정에 사용
   - 수동 설정 필요

6. **ADMIN_USERNAME** - ❌ 지우지 마세요! (하지만 선택)
   - railway.toml에서 자동 설정됨
   - Railway Variables에도 설정했다면 그대로 유지
   - 중복되어도 문제 없음 (Railway Variables 우선)

## 🗑️ 지워도 되는 항목

**없습니다!** 현재 백엔드에는 모든 환경 변수가 필요합니다.

## 📊 환경 변수 우선순위

Railway는 다음 순서로 환경 변수를 읽습니다:

1. **Railway Variables (최우선)** - 대시보드에서 설정한 값
2. **railway.toml의 [variables]** - 코드에서 정의된 값
3. **기본값** - 애플리케이션 코드의 기본값

따라서:
- Railway Variables에 설정한 모든 값이 유지됨
- railway.toml의 `ADMIN_USERNAME = "admin"`은 Railway Variables에 없을 때만 사용됨
- 둘 다 있다면 Railway Variables 값이 사용됨

## 💡 권장 사항

### 안전한 방법 (추천):
**모든 환경 변수를 Railway Variables에 유지하세요.**

이유:
- 보안상 안전함
- Railway 대시보드에서 쉽게 관리
- 일관성 유지

### 지워도 되는 특정 케이스:

`ADMIN_USERNAME`만 다음과 같은 상황에서 지워도 됩니다:
- Railway Variables에 `ADMIN_USERNAME`이 설정되어 있는 경우
- railway.toml의 자동 설정을 사용하고 싶은 경우

하지만 **다른 환경 변수는 절대 지우면 안 됩니다!**

## 🔍 확인 방법

Railway 대시보드에서:
1. 백엔드 서비스 선택
2. **Variables** 탭 클릭
3. 다음 항목이 모두 있는지 확인:
   - ✅ DATABASE_URL
   - ✅ SECRET_KEY
   - ✅ GEMINI_API_KEY
   - ✅ ADMIN_PASSWORD
   - ✅ FRONTEND_URL (프론트엔드 배포 후)
   - ✅ ADMIN_USERNAME (선택)

모두 있어야 정상입니다. **하나라도 빠지면 안 됩니다!**

