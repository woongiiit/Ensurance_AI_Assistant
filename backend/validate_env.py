#!/usr/bin/env python3
"""
환경 변수 검증 스크립트
Railway 배포 전 환경 변수가 올바르게 설정되었는지 확인합니다.
"""
import os
import sys

def validate_env():
    """환경 변수 검증"""
    errors = []
    warnings = []
    
    # 필수 환경 변수
    required_vars = {
        'DATABASE_URL': {
            'required': True,
            'description': 'PostgreSQL 데이터베이스 연결 URL',
            'validate': lambda x: x.startswith('postgresql://') or x.startswith('postgres://'),
            'error_msg': 'DATABASE_URL은 postgresql:// 또는 postgres://로 시작해야 합니다.'
        },
        'SECRET_KEY': {
            'required': True,
            'description': 'JWT 토큰 서명용 비밀 키',
            'validate': lambda x: len(x) >= 32 and not x.startswith('your-secret-key'),
            'error_msg': 'SECRET_KEY는 최소 32자 이상이어야 하며, 기본값을 사용하면 안 됩니다.',
            'warning_msg': 'SECRET_KEY가 너무 짧거나 기본값일 수 있습니다. 보안을 위해 강력한 랜덤 문자열을 사용하세요.'
        },
        'GEMINI_API_KEY': {
            'required': True,
            'description': 'Google Gemini API 키',
            'validate': lambda x: len(x) > 0 and not x.startswith('your-'),
            'error_msg': 'GEMINI_API_KEY를 설정해야 합니다.',
            'warning_msg': 'GEMINI_API_KEY가 기본값일 수 있습니다.'
        },
        'FRONTEND_URL': {
            'required': True,
            'description': '프론트엔드 서비스 URL (CORS 설정용)',
            'validate': lambda x: x.startswith('http://') or x.startswith('https://'),
            'error_msg': 'FRONTEND_URL은 http:// 또는 https://로 시작해야 합니다狭窄.'
        }
    }
    
    # 선택적 환경 변수
    optional_vars = {
        'ADMIN_USERNAME': {
            'default': 'admin',
            'description': '관리자 계정 이름'
        },
        'ADMIN_PASSWORD': {
            'default': 'admin123',
            'description': '관리자 계정 비밀번호',
            'validate': lambda x: len(x) >= 8 and x != 'admin123',
            'warning_msg': 'ADMIN_PASSWORD는 최소 8자 이상이어야 하며, 기본값(admin123)을 사용하면 안 됩니다.'
        },
        'VECTOR_DATABASE_URL': {
            'default': None,
            'description': '벡터 데이터베이스 URL (없으면 DATABASE_URL 사용)'
        }
    }
    
    print("🔍 환경 변수 검증 중...\n")
    
    # 필수 환경 변수 검증
    for var_name, config in required_vars.items():
        value = os.getenv(var_name)
        
        if not value:
            if config['required']:
                errors.append(f"❌ {var_name}: 설정되지 않음 - {config['description']}")
            continue
        
        # 값 검증
        if 'validate' in config:
            if not config['validate'](value):
                errors.append(f"❌ {var_name}: {config.get('error_msg', '유효하지 않은 값')}")
            elif 'warning_msg' in config:
                warnings.append(f"⚠️  {var_name}: {config['warning_msg']}")
        else:
            print(f"✅ {var_name}: 설정됨")
    
    # 선택적 환경 변수 검증
    for var_name, config in optional_vars.items():
        value = os.getenv(var_name, config.get('default'))
        
        if value:
            # 값 검증
            if 'validate' in config:
                if not config['validate'](value):
                    warnings.append(f"⚠️  {var_name}: {config.get('warning_msg', '유효하지 않은 값')}")
                else:
                    print(f"✅ {var_name}: 설정됨")
            else:
                print(f"✅ {var_name}: {value}")
    
    # 결과 출력
    print("\n" + "="*60)
    
    if warnings:
        print("\n⚠️  경고:")
        for warning in warnings:
            print(f"  {warning}")
    
    if errors:
        print("\n❌ 오류 (수정 필요):")
        for error in errors:
            print(f"  {error}")
        print("\n❌ 환경 변수 검증 실패!")
        return False
    
    if warnings and not errors:
        print("\n✅ 경고가 있지만 필수 환경 변수는 모두 설정되었습니다.")
        return True
    
    print("\n✅ 모든 환경 변수가 올바르게 설정되었습니다!")
    return True

if __name__ == '__main__':
    success = validate_env()
    sys.exit(0 if success else 1)

