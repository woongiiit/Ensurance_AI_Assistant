#!/usr/bin/env python3
"""
로컬 개발용 관리자 계정 초기화 스크립트
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.config import settings
from core.auth import get_password_hash
from models.database import AdminUser, Base

def init_admin_account():
    """관리자 계정 초기화"""
    # 데이터베이스 연결
    engine = create_engine(settings.database_url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # 테이블 생성
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # 기존 관리자 계정 확인
        existing_admin = db.query(AdminUser).filter(AdminUser.username == "admin").first()
        
        if existing_admin:
            print("✅ 관리자 계정이 이미 존재합니다.")
            print(f"   사용자명: {existing_admin.username}")
            return
        
        # 새 관리자 계정 생성
        admin_password = "admin123"
        hashed_password = get_password_hash(admin_password)
        
        admin_user = AdminUser(
            username="admin",
            hashed_password=hashed_password
        )
        
        db.add(admin_user)
        db.commit()
        
        print("🎉 관리자 계정이 성공적으로 생성되었습니다!")
        print("=" * 50)
        print("📋 로그인 정보:")
        print(f"   사용자명: admin")
        print(f"   비밀번호: {admin_password}")
        print("=" * 50)
        print("🌐 관리자 로그인 URL: http://localhost:3000/admin/login")
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_admin_account()
