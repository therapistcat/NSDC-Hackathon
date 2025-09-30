from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from datetime import datetime
from bson import ObjectId
from app.db.database import get_database
from app.api.routers.auth import get_current_user

router = APIRouter(prefix="/user", tags=["User Management & Dashboard"])

@router.get("/dashboard")
async def get_user_dashboard(
    current_user: dict = Depends(get_current_user)
):
    """Get comprehensive dashboard data for students (or mentor/recruiter view for recruiters)"""
    db = await get_database()
    
    if current_user["role"] == "student":
        return await get_student_dashboard(current_user, db)
    elif current_user["role"] == "recruiter":
        return await get_recruiter_dashboard(current_user, db)
    else:  # mentor
        return await get_mentor_dashboard(current_user, db)

async def get_student_dashboard(user: dict, db):
    """Get student-specific dashboard data"""
    
    # Get recent quiz attempts
    quiz_attempts = await db["quiz_attempts"].find(
        {"user_id": str(user["_id"])}
    ).sort("created_at", -1).limit(5).to_list(5)
    
    for attempt in quiz_attempts:
        attempt["_id"] = str(attempt["_id"])
    
    # Get badges earned
    badges = user.get("badges", [])
    
    # Get upcoming interviews
    upcoming_interviews = await db["interviews"].find({
        "student_id": str(user["_id"]),
        "status": "scheduled"
    }).sort("scheduled_time").limit(3).to_list(3)
    
    for interview in upcoming_interviews:
        interview["_id"] = str(interview["_id"])
    
    # Get community memberships
    communities = await db["communities"].find({
        "members": str(user["_id"])
    }).limit(5).to_list(5)
    
    # Get learning streak
    streak_info = await get_learning_streak(user)
    
    return {
        "user_profile": {
            "name": user["name"],
            "role": user["role"],
            "points": user.get("points", 0),
            "badges": badges,
            "streak_days": streak_info["current_streak"],
            "domains": user.get("domains", []),
            "skills": user.get("skills", []),
            "interests": user.get("interests", [])
        },
        "gamification": {
            "latest_quiz_attempts": quiz_attempts,
            "earned_badges": badges,
            "current_streak": streak_info["current_streak"],
            "points_earned": user.get("points", 0),
            "leaderboard_rank": await get_user_leaderboard_rank(user["_id"], db)
        },
        "learning": {
            "upcoming_interviews": upcoming_interviews,
            "community_memberships": [
                {
                    "id": str(c["_id"]),
                    "name": c["name"],
                    "topic": c["topic"],
                    "members_count": len(c.get("members", []))
                } for c in communities
            ],
            "learning_streak": streak_info["current_streak"]
        },
        "quick_actions": [
            "Take Daily Quiz",
            "Schedule Mock Interview",
            "Explore Communities",
            "View Learning Resources"
        ]
    }

async def get_recruiter_dashboard(user: dict, db):
    """Get recruiter dashboard with access to students' digital resumes"""
    
    # Get students who have completed interviews or have significant activity
    active_students = await db["users"].find({
        "role": "student",
        "$or": [
            {"points": {"$gte": 100}},
            {"badges": {"$exists": True, "$ne": []}}
        ]
    }).limit(20).to_list(20)
    
    student_profiles = []
    for student in active_students:
        student["_id"] = str(student["_id"])
        
        # Get student's recent activity
        quiz_count = len(student.get("quiz_attempts", []))
        interview_count = await db["interviews"].count_documents({
            "student_id": str(student["_id"]),
            "status": "completed"
        })
        
        # Create digital resume summary
        student_profiles.append({
            "id": student["_id"],
            "name": student["name"],
            "email": student.get("email"),
            "points": student.get("points", 0),
            "badges": student.get("badges", []),
            "domains": student.get("domains", []),
            "skills": student.get("skills", []),
            "quiz_attempts": quiz_count,
            "completed_interviews": interview_count,
            "communities_joined": await db["communities"].count_documents({
                "members": str(student["_id"])
            })
        })
    
    # Sort by activity score (points + badges + interviews)
    student_profiles.sort(key=lambda x: x["points"] + (len(x["badges"]) * 50) + (x["completed_interviews"] * 100), reverse=True)
    
    return {
        "dashboard_title": "Recruiter Dashboard - Student Talent Pool",
        "total_students_viewed": len(student_profiles),
        "top_talent": student_profiles[:10],
        "search_filters": {
            "domains": list(set([d for s in student_profiles for d in s["domains"]])),
            "skills": list(set([s for s in student_profiles for s in s["skills"]])),
            "badge_filter": ["Quiz Master", "Interview Ace", "Perfect Score", "Rising Star"]
        },
        "recruiter_actions": [
            "Search by skills/interests",
            "Download digital resumes",
            "Schedule placement drives",
            "View interview schedules"
        ]
    }

async def get_mentor_dashboard(user: dict, db):
    """Get mentor dashboard with students they're mentoring"""
    
    # Get interviews where user is mentor
    mentoring_sessions = await db["interviews"].find({
        "mentor_id": str(user["_id"])
    }).sort("scheduled_time", -1).limit(10).to_list(10)
    
    # Get unique students
    student_ids = set()
    recent_students = []
    
    for session in mentoring_sessions:
        if session["student_id"] not in student_ids:
            student = await db["users"].find_one({"_id": ObjectId(session["student_id"])  })
            if student and student not in recent_students:
                recent_students.append({
                    "id": str(student["_id"]),
                    "name": student["name"],
                    "progress": {
                        "points": student.get("points", 0),
                        "badges": len(student.get("badges", [])),
                        "quiz_attempts": len(student.get("quiz_attempts", []))
                    }
                })
                student_ids.add(session["student_id"])
    
    return {
        "mentor_profile": {
            "name": user["name"],
            "expertise": user.get("expertise", []),
            "experience_years": user.get("experience_years", 0),
            "availability": user.get("available", True)
        },
        "mentoring_stats": {
            "total_interviews_conducted": await db["interviews"].count_documents({
                "mentor_id": str(user["_id"]),
                "status": "completed"
            }),
            "upcoming_sessions": await db["interviews"].count_documents({
                "mentor_id": str(user["_id"]),
                "status": "scheduled"
            }),
            "active_mentees": len(recent_students)
        },
        "recent_mentees": recent_students[:5],
        "mentor_actions": [
            "Schedule new interview",
            "Rate previous sessions",
            "Create quiz content",
            "Update availability"
        ]
    }

async def get_learning_streak(user: dict) -> dict:
    """Get learning streak for user"""
    from datetime import timedelta
    db = await get_database()
    
    # Simplified streak calculation (last 30 days activity)
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    
    progress_count = await db["learning_progress"].count_documents({
        "user_id": str(user["_id"]),
        "viewed_at": {"$gte": thirty_days_ago}
    })
    
    return {
        "current_streak": min(progress_count, 30),
        "days_active_this_month": progress_count,
        "total_content_viewed": progress_count
    }

async def get_user_leaderboard_rank(user_id, db) -> int:
    """Get user's leaderboard rank"""
    users = await db["users"].find({"role": "student"}).sort("points", -1).to_list(None)
    
    for rank, user in enumerate(users, 1):
        if str(user["_id"]) == str(user_id):
            return rank
    
    return 0

@router.put("/profile")
async def update_user_profile(
    domains: Optional[str] = None,
    skills: Optional[str] = None,
    interests: Optional[str] = None,
    career_goal: Optional[str] = None,
    current_user: dict = Depends(get_current_user)
):
    """Update user profile information"""
    db = await get_database()
    
    update_data = {}
    
    if domains:
        update_data["domains"] = [d.strip() for d in domains.split(',')]
    if skills:
        update_data["skills"] = [s.strip() for s in skills.split(',')]
    if interests:
        update_data["interests"] = [i.strip() for i in interests.split(',')]
    if career_goal:
        update_data["career_goal"] = career_goal
    
    update_data["updated_at"] = datetime.utcnow()
    
    if update_data:
        result = await db["users"].update_one(
            {"_id": current_user["_id"]},
            {"$set": update_data}
        )
        
        if result.modified_count > 0:
            return {"message": "Profile updated successfully"}
    
    return {"message": "No changes made"}

@router.get("/progress")
async def get_user_progress(
    current_user: dict = Depends(get_current_user)
):
    """Get detailed user progress statistics"""
    db = await get_database()
    
    # Quiz statistics
    quiz_total = await db["quiz_attempts"].count_documents({"user_id": str(current_user["_id"])})
    quiz_scores = await db["quiz_attempts"].find(
        {"user_id": str(current_user["_id"])},
        {"final_score": 1}
    ).to_list(None)
    
    avg_quiz_score = 0
    if quiz_scores:
        total_score = sum([s.get("final_score", 0) for s in quiz_scores if s.get("final_score")])
        avg_quiz_score = total_score / len([s for s in quiz_scores if s.get("final_score") is not None])
    
    # Interview statistics
    completed_interviews = await db["interviews"].count_documents({
        "student_id": str(current_user["_id"]),
        "status": "completed"
    })
    
    return {
        "quiz_stats": {
            "total_quiz_attempts": quiz_total,
            "average_score": round(avg_quiz_score, 1),
            "best_score": max([(s.get("final_score", 0) for s in quiz_scores)], default=0)
        },
        "interview_stats": {
            "total_completed": completed_interviews,
            "upcoming": await db["interviews"].count_documents({
                "student_id": str(current_user["_id"]),
                "status": "scheduled"
            })
        },
        "learning_stats": {
            "content_viewed": await db["learning_progress"].count_documents({
                "user_id": str(current_user["_id"])
            }),
            "communities_joined": await db["communities"].count_documents({
                "members": str(current_user["_id"])
            })
        },
        "badges_earned": len(current_user.get("badges", [])),
        "current_rank": await get_user_leaderboard_rank(current_user["_id"], db)
    }

@router.post("/connect/mentor")
async def request_mentor_connection(
    mentor_id: str,
    message: str,
    current_user: dict = Depends(get_current_user)
):
    """Request connection to a mentor"""
    db = await get_database()
    
    # Verify mentor exists and is available
    try:
        mentor = await db["users"].find_one({
            "_id": ObjectId(mentor_id),
            "role": "mentor",
            "available": True
        })
    except:
        raise HTTPException(status_code=400, detail="Invalid mentor ID")
    
    if not mentor:
        raise HTTPException(status_code=404, detail="Mentor not found or unavailable")
    
    # Check if connection already exists
    existing_connection = await db["mentor_connections"].find_one({
        "student_id": str(current_user["_id"]),
        "mentor_id": mentor_id
    })
    
    if existing_connection:
        raise HTTPException(status_code=400, detail="Connection request already exists")
    
    # Create connection request
    connection_data = {
        "student_id": str(current_user["_id"]),
        "student_name": current_user["name"],
        "mentor_id": mentor_id,
        "mentor_name": mentor["name"],
        "status": "pending",
        "message": message,
        "student_skills": current_user.get("skills", []),
        "student_badges": current_user.get("badges", []),
        "created_at": datetime.utcnow()
    }
    
    result = await db["mentor_connections"].insert_one(connection_data)
    
    return {
        "connection_id": str(result.inserted_id),
        "message": "Connection request sent to mentor"
    }

@router.get("/mentor/connection-requests")
async def get_connection_requests(
    current_user: dict = Depends(get_current_user)
):
    """Mentors view connection requests"""
    if current_user["role"] != "mentor":
        raise HTTPException(status_code=403, detail="Only mentors can view connection requests")
    
    db = await get_database()
    
    requests = await db["mentor_connections"].find({
        "mentor_id": str(current_user["_id"])
    }).sort("created_at", -1).limit(20).to_list(20)
    
    for req in requests:
        req["_id"] = str(req["_id"])
    
    return requests

@router.put("/mentor/connection-request/{request_id}/{action}")
async def respond_to_connection_request(
    request_id: str,
    action: str,  # accept or reject
    current_user: dict = Depends(get_current_user)
):
    """Mentors accept or reject connection requests"""
    if current_user["role"] != "mentor":
        raise HTTPException(status_code=403, detail="Only mentors can respond to requests")
    
    if action not in ["accept", "reject"]:
        raise HTTPException(status_code=400, detail="Invalid action")
    
    db = await get_database()
    
    try:
        request = await db["mentor_connections"].find_one({"_id": ObjectId(request_id)})
    except:
        raise HTTPException(status_code=400, detail="Invalid request ID")
    
    if not request:
        raise HTTPException(status_code=404, detail="Connection request not found")
    
    if request["mentor_id"] != str(current_user["_id"]):
        raise HTTPException(status_code=403, detail="Not your request")
    
    await db["mentor_connections"].update_one(
        {"_id": ObjectId(request_id)},
        {
            "$set": {
                "status": "accepted" if action == "accept" else "rejected",
                "responded_at": datetime.utcnow()
            }
        }
    )
    
    return {"message": f"Connection request {'accepted' if action == 'accept' else 'rejected'}"}
