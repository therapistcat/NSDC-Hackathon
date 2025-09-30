from pydantic import BaseModel
from typing import List, Optional

class QuestionResponse(BaseModel):
    question: str
    options: List[str]
    correct_answer: Optional[str] = None

class QuizCreate(BaseModel):
    title: str
    difficulty: str
    questions: List[dict]

class QuizResponse(BaseModel):
    id: str
    title: str
    difficulty: str
    questions_count: int
    points: int
    time_limit: int

class QuizAttempt(BaseModel):
    quiz_id: str
    answers: List[dict]
    time_taken: int
    tab_switches: int = 0

class QuizAttemptResponse(BaseModel):
    attempt_id: str
    correct_answers: int
    total_questions: int
    score_percentage: float
    final_score: float
    points_earned: int
    badges_earned: List[str]
    next_recommended_difficulty: str
    message: str
