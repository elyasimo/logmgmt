from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError
from datetime import timedelta
from pydantic import BaseModel
from typing import Optional
import bcrypt
from ..dependencies import create_access_token, create_refresh_token, decode_token
from ..models import User, UserCreate, UserResponse, Token, AuthMethod
from ..database import get_db
from ..token_blacklist import token_blacklist
from ..config import ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS, LDAP_SERVER, AD_SERVER, AD_DOMAIN
from ..auth.ldap_auth import authenticate_ldap
from ..auth.ad_auth import authenticate_active_directory
from ..auth.sso_auth import authenticate_sso, oauth
from ..auth.azure_ad_auth import authenticate_azure_ad
import re

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class RefreshTokenRequest(BaseModel):
    refresh_token: str

def get_password_hash(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_token(token)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = db.query(User).filter(User.username == token_data.username).first()
    if user is None:
        raise credentials_exception
    return user

def check_password_strength(password: str) -> bool:
    if len(password) < 8:
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'\d', password):
        return False
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False
    return True

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

@router.post("/register", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    if user.auth_method == AuthMethod.local:
        if not user.password:
            raise HTTPException(status_code=400, detail="Password is required for local authentication")
        if not check_password_strength(user.password):
            raise HTTPException(
                status_code=400,
                detail="Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one digit, and one special character."
            )
        hashed_password = get_password_hash(user.password)
    else:
        hashed_password = None
    
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        auth_method=user.auth_method,
        external_id=user.external_id
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    if user.auth_method == AuthMethod.local:
        if not verify_password(form_data.password, user.hashed_password):
            raise HTTPException(status_code=400, detail="Incorrect username or password")
    elif user.auth_method == AuthMethod.ldap:
        if not authenticate_ldap(user.username, form_data.password, LDAP_SERVER):
            raise HTTPException(status_code=400, detail="LDAP authentication failed")
    elif user.auth_method == AuthMethod.active_directory:
        if not authenticate_active_directory(user.username, form_data.password, AD_SERVER, AD_DOMAIN):
            raise HTTPException(status_code=400, detail="Active Directory authentication failed")
    elif user.auth_method == AuthMethod.sso:
        raise HTTPException(status_code=400, detail="SSO users should use the /login/google endpoint")
    elif user.auth_method == AuthMethod.azure_ad:
        result = authenticate_azure_ad(user.username, form_data.password)
        if not result["success"]:
            raise HTTPException(status_code=400, detail="Azure AD authentication failed")
    else:
        raise HTTPException(status_code=400, detail="Unsupported authentication method")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(
        data={"sub": user.username}, expires_delta=refresh_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer", "refresh_token": refresh_token}

@router.get('/login/google')
async def login_google(request: Request):
    redirect_uri = request.url_for('auth_google')
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get('/auth/google')
async def auth_google(request: Request, db: Session = Depends(get_db)):
    user = await authenticate_sso(request)
    if user:
        db_user = db.query(User).filter(User.email == user['email']).first()
        if not db_user:
            db_user = User(
                username=user['email'],
                email=user['email'],
                auth_method=AuthMethod.sso,
                external_id=user['sub']
            )
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
        
        access_token = create_access_token(data={"sub": db_user.username})
        refresh_token = create_refresh_token(data={"sub": db_user.username})
        return {"access_token": access_token, "token_type": "bearer", "refresh_token": refresh_token}
    raise HTTPException(status_code=400, detail="SSO authentication failed")

@router.post("/logout")
async def logout(token: str = Depends(oauth2_scheme)):
    token_blacklist.add_token(token, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"message": "Successfully logged out"}

@router.post("/refresh", response_model=Token)
async def refresh_token(refresh_request: RefreshTokenRequest):
    try:
        payload = decode_token(refresh_request.refresh_token)
        username: str = payload.get("sub")
        is_refresh_token: bool = payload.get("refresh", False)
        if username is None or not is_refresh_token:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
        
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": username}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer", "refresh_token": refresh_request.refresh_token}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@router.put("/me", response_model=UserResponse)
async def update_user(
    user_update: UserCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    if user_update.username != current_user.username:
        if db.query(User).filter(User.username == user_update.username).first():
            raise HTTPException(status_code=400, detail="Username already registered")
    
    if user_update.email != current_user.email:
        if db.query(User).filter(User.email == user_update.email).first():
            raise HTTPException(status_code=400, detail="Email already registered")
    
    current_user.username = user_update.username
    current_user.email = user_update.email
    
    if user_update.password:
        if not check_password_strength(user_update.password):
            raise HTTPException(
                status_code=400,
                detail="Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one digit, and one special character."
            )
        current_user.hashed_password = get_password_hash(user_update.password)
    
    db.commit()
    db.refresh(current_user)
    return current_user

class TokenData(BaseModel):
    username: Optional[str] = None

