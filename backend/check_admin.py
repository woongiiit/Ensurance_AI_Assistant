#!/usr/bin/env python3
"""
관리자 계정 확인 스크립트
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.config import settings
from models.database import AdminUser

def check_admin_account():
    """관리자 계정 확인"""
    engine = create_engine(settings.database_url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    db = SessionLocal()
    
    try:
        admin = db.query(AdminUser).filter(AdminUser.username == "admin").first()
        
        if admin:
            print("✅ 관리자 계정이 존재합니다!")
            print(f"   ID: {admin.id}")
            print(f"   사용자명: {admin.username}")
            print("   비밀번호: admin123")
        else:
            print("❌ 관리자 계정이 없습니다.")
            
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check_admin_account()
