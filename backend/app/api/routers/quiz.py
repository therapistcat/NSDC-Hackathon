from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from datetime import datetime
from bson import ObjectId
from app.db.database import get_database
from app.api.routers.auth import get_current_user
from app.db.schemas.quiz_schema import (
    QuizCreate, QuizResponse, QuizAttempt, QuizAttemptResponse,
    QuestionResponse
)

router = APIRouter(prefix="/quiz", tags=["Quiz & Gamification"])

@router.post("/create", response_model=QuizResponse)
async def create_quiz(
    title: str,
    difficulty: str,  # easy, medium, hard
    questions: List[dict],
    current_user: dict = Depends(get_current_user)
):
    """Create a new quiz (admin/mentor only)"""
    if current_user["role"] not in ["mentor", "recruiter"]:
        raise HTTPException(status_code=403, detail="Only mentors/recruiters can create quizzes")
    
    db = await get_database()
    
    # Calculate points based on difficulty
    points_map = {"easy": 10, "medium": 20, "hard": 30}
    time_limit_map = {"easy": 30, "medium": 45, "hard": 60}  # seconds per question
    
    quiz_data = {
        "title": title,
        "difficulty": difficulty,
        "questions": questions,
        "points": points_map.get(difficulty, 10),
        "time_limit": time_limit_map.get(difficulty, 30) * len(questions),
        "created_by": str(current_user["_id"]),
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    result = await db["quizzes"].insert_one(quiz_data)
    quiz_data["_id"] = str(result.inserted_id)
    
    return QuizResponse(
        id=str(result.inserted_id),
        title=title,
        difficulty=difficulty,
        questions_count=len(questions),
        points=quiz_data["points"],
        time_limit=quiz_data["time_limit"]
    )

@router.get("/available", response_model=List[QuizResponse])
async def get_available_quizzes(
    difficulty: Optional[str] = None,
    current_user: dict = Depends(get_current_user)
):
    """Get available quizzes for students"""
    db = await get_database()
    
    query = {}
    if difficulty:
        query["difficulty"] = difficulty
    
    quizzes = await db["quizzes"].find(query).to_list(100)
    
    return [
        QuizResponse(
            id=str(quiz["_id"]),
            title=quiz["title"],
            difficulty=quiz["difficulty"],
            questions_count=len(quiz["questions"]),
            points=quiz["points"],
            time_limit=quiz.get("time_limit", 300)
        )
        for quiz in quizzes
    ]

@router.get("/{quiz_id}", response_model=dict)
async def get_quiz(
    quiz_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get a specific quiz with questions"""
    db = await get_database()
    
    try:
        quiz = await db["quizzes"].find_one({"_id": ObjectId(quiz_id)})
    except:
        raise HTTPException(status_code=400, detail="Invalid quiz ID")
    
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    quiz["_id"] = str(quiz["_id"])
    return quiz

@router.post("/attempt", response_model=QuizAttemptResponse)
async def attempt_quiz(
    quiz_id: str,
    answers: List[dict],  # [{"question_id": 0, "answer": "A"}]
    time_taken: int,  # seconds
    tab_switches: int = 0,
    current_user: dict = Depends(get_current_user)
):
    """Submit quiz attempt and calculate score with reinforcement learning principles"""
    db = await get_database()
    
    # Get quiz
    try:
        quiz = await db["quizzes"].find_one({"_id": ObjectId(quiz_id)})
    except:
        raise HTTPException(status_code=400, detail="Invalid quiz ID")
    
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    # Calculate score
    correct_answers = 0
    total_questions = len(quiz["questions"])
    
    for answer in answers:
        question_idx = answer["question_id"]
        if question_idx < len(quiz["questions"]):
            correct_answer = quiz["questions"][question_idx].get("correct_answer")
            if answer["answer"] == correct_answer:
                correct_answers += 1
    
    # Calculate base score percentage
    score_percentage = (correct_answers / total_questions) * 100 if total_questions > 0 else 0
    
    # Apply penalties
    time_limit = quiz.get("time_limit", 300)
    time_penalty = max(0, (time_taken - time_limit) // 60) * 5  # -5% per extra minute
    tab_switch_penalty = tab_switches * 10  # -10% per tab switch
    
    final_score = max(0, score_percentage - time_penalty - tab_switch_penalty)
    
    # Calculate points earned
    base_points = quiz["points"]
    points_earned = int((final_score / 100) * base_points)
    
    # Reinforcement Learning: Adjust difficulty recommendation
    if score_percentage >= 80:
        next_difficulty = "hard" if quiz["difficulty"] != "hard" else "hard"
    elif score_percentage >= 50:
        next_difficulty = quiz["difficulty"]
    else:
        next_difficulty = "easy" if quiz["difficulty"] != "easy" else "easy"
    
    # Save attempt
    attempt_data = {
        "user_id": str(current_user["_id"]),
        "quiz_id": quiz_id,
        "answers": answers,
        "correct_answers": correct_answers,
        "total_questions": total_questions,
        "score_percentage": score_percentage,
        "final_score": final_score,
        "points_earned": points_earned,
        "time_taken": time_taken,
        "time_limit": time_limit,
        "tab_switches": tab_switches,
        "penalties": {
            "time_penalty": time_penalty,
            "tab_switch_penalty": tab_switch_penalty
        },
        "next_recommended_difficulty": next_difficulty,
        "created_at": datetime.utcnow()
    }
    
    result = await db["quiz_attempts"].insert_one(attempt_data)
    
    # Update user points and badges
    await db["users"].update_one(
        {"_id": current_user["_id"]},
        {
            "$inc": {"points": points_earned},
            "$push": {"quiz_attempts": str(result.inserted_id)},
            "$set": {"updated_at": datetime.utcnow()}
        }
    )
    
    # Check and award badges
    user = await db["users"].find_one({"_id": current_user["_id"]})
    badges_earned = []
    
    # Badge logic
    quiz_attempts_count = len(user.get("quiz_attempts", []))
    if quiz_attempts_count >= 10 and "Quiz Master" not in user.get("badges", []):
        badges_earned.append("Quiz Master")
    
    if final_score == 100 and "Perfect Score" not in user.get("badges", []):
        badges_earned.append("Perfect Score")
    
    if user.get("points", 0) >= 500 and "Rising Star" not in user.get("badges", []):
        badges_earned.append("Rising Star")
    
    if badges_earned:
        await db["users"].update_one(
            {"_id": current_user["_id"]},
            {"$addToSet": {"badges": {"$each": badges_earned}}}
        )
    
    return QuizAttemptResponse(
        attempt_id=str(result.inserted_id),
        correct_answers=correct_answers,
        total_questions=total_questions,
        score_percentage=score_percentage,
        final_score=final_score,
        points_earned=points_earned,
        badges_earned=badges_earned,
        next_recommended_difficulty=next_difficulty,
        message=f"Quiz completed! You scored {final_score:.1f}%"
    )

@router.get("/attempts/history", response_model=List[dict])
async def get_quiz_history(
    current_user: dict = Depends(get_current_user)
):
    """Get user's quiz attempt history"""
    db = await get_database()
    
    attempts = await db["quiz_attempts"].find(
        {"user_id": str(current_user["_id"])}
    ).sort("created_at", -1).to_list(50)
    
    for attempt in attempts:
        attempt["_id"] = str(attempt["_id"])
    
    return attempts

@router.get("/leaderboard", response_model=List[dict])
async def get_leaderboard(limit: int = 10):
    """Get quiz leaderboard"""
    db = await get_database()
    
    users = await db["users"].find(
        {"role": "student"}
    ).sort("points", -1).limit(limit).to_list(limit)
    
    leaderboard = []
    for idx, user in enumerate(users, 1):
        leaderboard.append({
            "rank": idx,
            "name": user["name"],
            "points": user.get("points", 0),
            "badges": user.get("badges", []),
            "quiz_attempts": len(user.get("quiz_attempts", []))
        })
    
    return leaderboard
