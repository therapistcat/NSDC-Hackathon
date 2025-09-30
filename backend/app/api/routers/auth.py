from fastapi import APIRouter, Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.db.database import get_database
from app.core.config import settings
from app.db.models.user import User
from app.db.schemas.user_schemas import UserCreate, UserResponse, Token
from passlib.context import CryptContext

router = APIRouter(prefix="/auth", tags=["Authentication"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    db = await get_database()
    user = await db["users"].find_one({"email": email})
    if user is None:
        raise credentials_exception
    return user

@router.post("/student/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def student_signup(
    signup_data: Dict[str, Any] = Body(...)
):
    """Register a new student with their domains, skills, and interests"""
    db = await get_database()

    # Extract values from request data
    name = signup_data.get("name")
    email = signup_data.get("email")
    password = signup_data.get("password")
    domains = signup_data.get("domains")
    skills = signup_data.get("skills")
    interests = signup_data.get("interests")

    # Check if user exists
    existing_user = await db["users"].find_one({"email": email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Parse tags from domains, skills, and interests
    tags = []
    if domains:
        tags.extend([d.strip() for d in domains.split(',')])
    if skills:
        tags.extend([s.strip() for s in skills.split(',')])
    if interests:
        tags.extend([i.strip() for i in interests.split(',')])

    # Create new user
    hashed_password = get_password_hash(password)
    new_user = {
        "name": name,
        "email": email,
        "password": hashed_password,
        "role": "student",
        "tags": tags,
        "domains": [d.strip() for d in domains.split(',')] if domains else [],
        "skills": [s.strip() for s in skills.split(',')] if skills else [],
        "interests": [i.strip() for i in interests.split(',')] if interests else [],
        "points": 0,
        "badges": [],
        "streak": 0,
        "quiz_attempts": [],
        "mock_interviews": [],
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }

    result = await db["users"].insert_one(new_user)
    new_user["_id"] = str(result.inserted_id)

    return UserResponse(
        id=str(result.inserted_id),
        name=name,
        email=email,
        role="student",
        message="Student registered successfully"
    )

@router.post("/recruiter/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def recruiter_signup(
    signup_data: Dict[str, Any] = Body(...)
):
    """Register a new recruiter"""
    db = await get_database()

    name = signup_data.get("name")
    email = signup_data.get("email")
    password = signup_data.get("password")
    company = signup_data.get("company")
    position = signup_data.get("position")

    # Check if user exists
    existing_user = await db["users"].find_one({"email": email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create new user
    hashed_password = get_password_hash(password)
    new_user = {
        "name": name,
        "email": email,
        "password": hashed_password,
        "role": "recruiter",
        "company": company,
        "position": position,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }

    result = await db["users"].insert_one(new_user)

    return UserResponse(
        id=str(result.inserted_id),
        name=name,
        email=email,
        role="recruiter",
        message="Recruiter registered successfully"
    )

@router.post("/mentor/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def mentor_signup(
    signup_data: Dict[str, Any] = Body(...)
):
    """Register a new mentor"""
    db = await get_database()

    name = signup_data.get("name")
    email = signup_data.get("email")
    password = signup_data.get("password")
    expertise = signup_data.get("expertise")
    experience_years = signup_data.get("experience_years")

    # Check if user exists
    existing_user = await db["users"].find_one({"email": email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create new user
    hashed_password = get_password_hash(password)
    new_user = {
        "name": name,
        "email": email,
        "password": hashed_password,
        "role": "mentor",
        "expertise": [e.strip() for e in expertise.split(',')] if expertise else [],
        "experience_years": experience_years,
        "available": True,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }

    result = await db["users"].insert_one(new_user)

    return UserResponse(
        id=str(result.inserted_id),
        name=name,
        email=email,
        role="mentor",
        message="Mentor registered successfully"
    )

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login endpoint for all user types"""
    db = await get_database()
    
    user = await db["users"].find_one({"email": form_data.username})
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["email"], "role": user["role"]}, 
        expires_delta=access_token_expires
    )
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        user_id=str(user["_id"]),
        role=user["role"]
    )

@router.get("/me")
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """Get current logged-in user information"""
    current_user["_id"] = str(current_user["_id"])
    current_user.pop("password", None)
    return current_user
