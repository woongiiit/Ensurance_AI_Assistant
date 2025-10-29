from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from core.config import settings
from core.database import get_db
from core.auth import authenticate_admin, create_access_token, get_password_hash
from models.database import AdminUser
from schemas.api import LoginRequest, TokenResponse

router = APIRouter()


@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    """Admin login endpoint"""
    admin = authenticate_admin(db, request.username, request.password)
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": admin.username}, expires_delta=access_token_expires
    )
    
    return TokenResponse(access_token=access_token, token_type="bearer")


@router.post("/init-admin")
async def init_admin(db: Session = Depends(get_db)):
    """Initialize admin user (for development only)"""
    # Check if admin already exists
    existing_admin = db.query(AdminUser).filter(AdminUser.username == settings.admin_username).first()
    if existing_admin:
        return {"message": "Admin user already exists"}
    
    # Create admin user
    hashed_password = get_password_hash(settings.admin_password)
    admin = AdminUser(
        username=settings.admin_username,
        hashed_password=hashed_password
    )
    db.add(admin)
    db.commit()
    
    return {"message": "Admin user created successfully"}

