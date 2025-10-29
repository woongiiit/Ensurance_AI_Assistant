#!/usr/bin/env python3
"""
간단한 해시로 관리자 계정 생성
"""

import hashlib
from sqlalchemy import create_engine, text

def create_admin_simple():
    """간단한 해시로 관리자 계정 생성"""
    # SQLite 데이터베이스 연결
    engine = create_engine("sqlite:///./insurance_rag.db")
    
    try:
        # 간단한 해시 생성 (실제 운영에서는 bcrypt 사용)
        admin_password = "admin123"
        password_hash = hashlib.sha256(admin_password.encode()).hexdigest()
        
        with engine.connect() as conn:
            # 테이블 생성
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS admin_users (
                    id INTEGER PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    hashed_password VARCHAR(255) NOT NULL
                )
            """))
            
            # 기존 관리자 계정 삭제
            conn.execute(text("DELETE FROM admin_users WHERE username = 'admin'"))
            
            # 새 관리자 계정 삽입
            conn.execute(text("""
                INSERT INTO admin_users (username, hashed_password) 
                VALUES ('admin', :password)
            """), {"password": password_hash})
            
            conn.commit()
        
        print("🎉 관리자 계정이 성공적으로 생성되었습니다!")
        print("=" * 50)
        print("📋 로그인 정보:")
        print(f"   사용자명: admin")
        print(f"   비밀번호: {admin_password}")
        print("=" * 50)
        print("🌐 관리자 로그인 URL: http://localhost:3000/admin/login")
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")

if __name__ == "__main__":
    create_admin_simple()
