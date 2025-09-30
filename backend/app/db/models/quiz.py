from typing import List
from .base import MongoBaseModel

class Quiz(MongoBaseModel):
    title: str
    questions: List[dict]
    difficulty: str
    points: int