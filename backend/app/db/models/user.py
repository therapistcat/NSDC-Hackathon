from typing import Optional, List
from pydantic import EmailStr
from .base import MongoBaseModel

class User(MongoBaseModel):
    name: str
    email: EmailStr
    password: str
    role: str
    tags: Optional[List[str]] = []
    points: int = 0
    badges: List[str] = []
