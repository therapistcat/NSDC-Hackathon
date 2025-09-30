from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from app.db.database import get_database
from app.core.config import DATABASE_NAME
from app.db.models.user import User
from passlib.context import CryptContext

router = APIRouter(prefix="/auth")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/student/signup")
async def student_signup(name: str, email: str, password: str, tags: str):
    db = await get_database()
    collection = db[DATABASE_NAME]["users"]
    
    # Check if user exists
    existing_user = await collection.find_one({"email": email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create new user
    hashed_password = pwd_context.hash(password)
    new_user = User(
        name=name,
        email=email,
        password=hashed_password,
        role="student",
        tags=tags.split(',')
    )
    
    result = await collection.insert_one(new_user.dict(exclude={'id'}))
    
    return {"msg": "Student registered successfully", "user_id": str(result.inserted_id)}

@router.post("/recruiter/signup")
async def recruiter_signup(name: str, email: str, password: str):
    db = await get_database()
    collection = db[DATABASE_NAME]["users"]
    
    # Check if user exists
    existing_user = await collection.find_one({"email": email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create new user
    hashed_password = pwd_context.hash(password)
    new_user = User(
        name=name,
        email=email,
        password=hashed_password,
        role="recruiter"
    )
    
    result = await collection.insert_one(new_user.dict(exclude={'id'}))
    
    return {"msg": "Recruiter registered successfully", "user_id": str(result.inserted_id)}

@router.post("/mentor/signup")
async def mentor_signup(name: str, email: str, password: str):
    db = await get_database()
    collection = db[DATABASE_NAME]["users"]
    
    # Check if user exists
    existing_user = await collection.find_one({"email": email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create new user
    hashed_password = pwd_context.hash(password)
    new_user = User(
        name=name,
        email=email,
        password=hashed_password,
        role="mentor"
    )
    
    result = await collection.insert_one(new_user.dict(exclude={'id'}))
    
    return {"msg": "Mentor registered successfully", "user_id": str(result.inserted_id)}
