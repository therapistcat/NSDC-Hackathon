from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from datetime import datetime, timedelta
from bson import ObjectId
from app.db.database import get_database
from app.api.routers.auth import get_current_user

router = APIRouter(prefix="/interview", tags=["Mock Interviews"])

@router.post("/schedule")
async def schedule_mock_interview(
    mentor_id: str,
    scheduled_time: str,  # ISO format datetime string
    topic: str,
    difficulty: str,
    current_user: dict = Depends(get_current_user)
):
    """Schedule a mock interview (requires badges)"""
    db = await get_database()
    
    # Check if user has enough badges (apex badges requirement)
    user_badges = current_user.get("badges", [])
    required_badges = 3  # Minimum badges to unlock interview feature
    
    if len(user_badges) < required_badges:
        raise HTTPException(
            status_code=403,
            detail=f"You need at least {required_badges} badges to schedule interviews. Current: {len(user_badges)}"
        )
    
    # Verify mentor exists
    try:
        mentor = await db["users"].find_one({"_id": ObjectId(mentor_id), "role": "mentor"})
    except:
        raise HTTPException(status_code=400, detail="Invalid mentor ID")
    
    if not mentor:
        raise HTTPException(status_code=404, detail="Mentor not found")
    
    # Create interview
    interview_data = {
        "student_id": str(current_user["_id"]),
        "student_name": current_user["name"],
        "mentor_id": mentor_id,
        "mentor_name": mentor["name"],
        "scheduled_time": datetime.fromisoformat(scheduled_time.replace('Z', '+00:00')),
        "topic": topic,
        "difficulty": difficulty,
        "status": "scheduled",
        "score": None,
        "feedback": None,
        "recording_url": None,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    result = await db["interviews"].insert_one(interview_data)
    
    # Update user's mock_interviews list
    await db["users"].update_one(
        {"_id": current_user["_id"]},
        {
            "$push": {"mock_interviews": str(result.inserted_id)},
            "$set": {"updated_at": datetime.utcnow()}
        }
    )
    
    return {
        "interview_id": str(result.inserted_id),
        "message": "Mock interview scheduled successfully",
        "scheduled_time": scheduled_time,
        "mentor_name": mentor["name"]
    }

@router.get("/my-interviews")
async def get_my_interviews(
    status: Optional[str] = None,
    current_user: dict = Depends(get_current_user)
):
    """Get all interviews for current user"""
    db = await get_database()
    
    query = {"student_id": str(current_user["_id"])}
    if status:
        query["status"] = status
    
    interviews = await db["interviews"].find(query).sort("scheduled_time", -1).to_list(50)
    
    for interview in interviews:
        interview["_id"] = str(interview["_id"])
    
    return interviews

@router.get("/mentor/interviews")
async def get_mentor_interviews(
    status: Optional[str] = None,
    current_user: dict = Depends(get_current_user)
):
    """Get all interviews for mentor"""
    if current_user["role"] != "mentor":
        raise HTTPException(status_code=403, detail="Only mentors can access this")
    
    db = await get_database()
    
    query = {"mentor_id": str(current_user["_id"])}
    if status:
        query["status"] = status
    
    interviews = await db["interviews"].find(query).sort("scheduled_time", -1).to_list(50)
    
    for interview in interviews:
        interview["_id"] = str(interview["_id"])
    
    return interviews

@router.put("/{interview_id}/complete")
async def complete_interview(
    interview_id: str,
    score: float,
    feedback: str,
    strengths: str,
    improvements: str,
    current_user: dict = Depends(get_current_user)
):
    """Complete an interview and provide score/feedback (mentor only)"""
    if current_user["role"] != "mentor":
        raise HTTPException(status_code=403, detail="Only mentors can complete interviews")
    
    db = await get_database()
    
    try:
        interview = await db["interviews"].find_one({"_id": ObjectId(interview_id)})
    except:
        raise HTTPException(status_code=400, detail="Invalid interview ID")
    
    if not interview:
        raise HTTPException(status_code=404, detail="Interview not found")
    
    if interview["mentor_id"] != str(current_user["_id"]):
        raise HTTPException(status_code=403, detail="Not your interview")
    
    # Update interview
    await db["interviews"].update_one(
        {"_id": ObjectId(interview_id)},
        {
            "$set": {
                "status": "completed",
                "score": score,
                "feedback": feedback,
                "strengths": strengths,
                "improvements": improvements,
                "completed_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
        }
    )
    
    # Award badges based on performance
    student = await db["users"].find_one({"_id": ObjectId(interview["student_id"])})
    badges_earned = []
    
    if score >= 90 and "Interview Ace" not in student.get("badges", []):
        badges_earned.append("Interview Ace")
    
    if score >= 80 and "Strong Communicator" not in student.get("badges", []):
        badges_earned.append("Strong Communicator")
    
    # Count completed interviews
    completed_interviews = await db["interviews"].count_documents({
        "student_id": interview["student_id"],
        "status": "completed"
    })
    
    if completed_interviews >= 5 and "Interview Expert" not in student.get("badges", []):
        badges_earned.append("Interview Expert")
    
    if badges_earned:
        await db["users"].update_one(
            {"_id": ObjectId(interview["student_id"])},
            {"$addToSet": {"badges": {"$each": badges_earned}}}
        )
    
    return {
        "message": "Interview completed successfully",
        "score": score,
        "badges_earned": badges_earned
    }

@router.get("/{interview_id}")
async def get_interview_details(
    interview_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get interview details"""
    db = await get_database()
    
    try:
        interview = await db["interviews"].find_one({"_id": ObjectId(interview_id)})
    except:
        raise HTTPException(status_code=400, detail="Invalid interview ID")
    
    if not interview:
        raise HTTPException(status_code=404, detail="Interview not found")
    
    # Check authorization
    user_id = str(current_user["_id"])
    if interview["student_id"] != user_id and interview["mentor_id"] != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to view this interview")
    
    interview["_id"] = str(interview["_id"])
    
    return interview

@router.delete("/{interview_id}")
async def cancel_interview(
    interview_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Cancel a scheduled interview"""
    db = await get_database()
    
    try:
        interview = await db["interviews"].find_one({"_id": ObjectId(interview_id)})
    except:
        raise HTTPException(status_code=400, detail="Invalid interview ID")
    
    if not interview:
        raise HTTPException(status_code=404, detail="Interview not found")
    
    if interview["student_id"] != str(current_user["_id"]):
        raise HTTPException(status_code=403, detail="Can only cancel your own interviews")
    
    if interview["status"] != "scheduled":
        raise HTTPException(status_code=400, detail="Can only cancel scheduled interviews")
    
    await db["interviews"].update_one(
        {"_id": ObjectId(interview_id)},
        {
            "$set": {
                "status": "cancelled",
                "updated_at": datetime.utcnow()
            }
        }
    )
    
    return {"message": "Interview cancelled successfully"}

@router.get("/stats/performance")
async def get_interview_stats(current_user: dict = Depends(get_current_user)):
    """Get interview performance statistics"""
    db = await get_database()
    
    interviews = await db["interviews"].find({
        "student_id": str(current_user["_id"]),
        "status": "completed"
    }).to_list(100)
    
    if not interviews:
        return {
            "total_interviews": 0,
            "average_score": 0,
            "highest_score": 0,
            "topics_covered": []
        }
    
    scores = [i["score"] for i in interviews if i.get("score")]
    topics = list(set(i["topic"] for i in interviews))
    
    return {
        "total_interviews": len(interviews),
        "average_score": sum(scores) / len(scores) if scores else 0,
        "highest_score": max(scores) if scores else 0,
        "topics_covered": topics
    }
