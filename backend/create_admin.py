#!/usr/bin/env python3
"""
직접 관리자 계정 생성 스크립트
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from core.config import settings
from core.auth import get_password_hash

def create_admin_directly():
    """직접 관리자 계정 생성"""
    engine = create_engine(settings.database_url)
    
    try:
        # 비밀번호 해시 생성
        admin_password = "admin123"
        hashed_password = get_password_hash(admin_password)
        
        # 직접 SQL로 관리자 계정 생성
        with engine.connect() as conn:
            # 테이블이 없으면 생성
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS admin_users (
                    id INTEGER PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    hashed_password VARCHAR(255) NOT NULL
                )
            """))
            
            # 기존 관리자 계정 삭제 (있다면)
            conn.execute(text("DELETE FROM admin_users WHERE username = 'admin'"))
            
            # 새 관리자 계정 삽입
            conn.execute(text("""
                INSERT INTO admin_users (username, hashed_password) 
                VALUES ('admin', :password)
            """), {"password": hashed_password})
            
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
    create_admin_directly()
