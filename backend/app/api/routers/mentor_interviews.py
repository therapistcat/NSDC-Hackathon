from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from datetime import datetime
from bson import ObjectId
from app.db.database import get_database
from app.api.routers.auth import get_current_user

router = APIRouter(prefix="/mentor-interviews", tags=["Mentor Interview Management"])

@router.post("/connect/{student_id}")
async def initiate_mentor_connect(
    student_id: str,
    call_type: str = "video",  # video, audio, chat
    current_user: dict = Depends(get_current_user)
):
    """Direct connect to mentor via video/audio call (unlocked with badges)"""
    db = await get_database()
    
    # Verify user has required badges
    user_badges = current_user.get("badges", [])
    required_badges = 5  # Minimum badges required for direct mentor connect
    
    if len(user_badges) < required_badges:
        raise HTTPException(
            status_code=403,
            detail=f"You need at least {required_badges} badges for direct mentor connect. Current: {len(user_badges)}"
        )
    
    # Verify student (can only connect as student role)
    if current_user["role"] != "student":
        raise HTTPException(status_code=403, detail="Only students can initiate mentor connects")
    
    # Find available mentor matching student's skills
    student_skills = current_user.get("skills", [])
    student_domains = current_user.get("domains", [])
    
    # Query mentors with matching expertise (simple overlap for now)
    available_mentors = await db["users"].find({
        "role": "mentor",
        "available": True
    }).to_list(20)
    
    # Score mentors based on skill match
    scored_mentors = []
    for mentor in available_mentors:
        mentor_expertise = mentor.get("expertise", [])
        skill_overlap = len(set(student_skills) & set(mentor_expertise))
        domain_overlap = len(set(student_domains) & set(mentor_expertise))
        
        if skill_overlap > 0 or domain_overlap > 0:
            mentor["match_score"] = skill_overlap + domain_overlap
            mentor["skill_overlap"] = skill_overlap
            mentor["domain_overlap"] = domain_overlap
            scored_mentors.append(mentor)
    
    if not scored_mentors:
        raise HTTPException(
            status_code=404,
            detail="No suitable mentors available for your skill set. Please schedule formal interviews instead."
        )
    
    # Select best matching mentor
    best_mentor = sorted(scored_mentors, key=lambda x: x["match_score"], reverse=True)[0]
    
    # Create direct mentor connect session
    connect_session = {
        "student_id": str(current_user["_id"]),
        "student_name": current_user["name"],
        "mentor_id": str(best_mentor["_id"]),
        "mentor_name": best_mentor["name"],
        "call_type": call_type,
        "status": "initiated",
        "connection_reason": "direct_connect_via_badges",
        "student_skills": student_skills,
        "matched_expertise": list(set(student_skills) & set(best_mentor.get("expertise", []))),
        "session_rating": None,
        "session_feedback": None,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    result = await db["mentor_connects"].insert_one(connect_session)
    
    # Update mentor availability temporarily
    await db["users"].update_one(
        {"_id": best_mentor["_id"]},
        {"$set": {"available": False}}
    )
    
    return {
        "connect_session_id": str(result.inserted_id),
        "mentor_name": best_mentor["name"],
        "matched_expertise": connect_session["matched_expertise"],
        "call_type": call_type,
        "message": f"Direct connect initiated with mentor {best_mentor['name']}. They will be notified."
    }

@router.put("/session/{session_id}/start")
async def start_mentor_session(
    session_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Start the mentor connect session"""
    db = await get_database()
    
    try:
        session = await db["mentor_connects"].find_one({"_id": ObjectId(session_id)})
    except:
        raise HTTPException(status_code=400, detail="Invalid session ID")
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Verify user is the mentor or student of this session
    user_id = str(current_user["_id"])
    if user_id not in [session["student_id"], session["mentor_id"]]:
        raise HTTPException(status_code=403, detail="Not authorized for this session")
    
    if session["status"] != "initiated":
        raise HTTPException(status_code=400, detail="Session cannot be started")
    
    await db["mentor_connects"].update_one(
        {"_id": ObjectId(session_id)},
        {
            "$set": {
                "status": "active",
                "started_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
        }
    )
    
    return {"message": "Session started successfully"}

@router.put("/session/{session_id}/complete")
async def complete_mentor_session(
    session_id: str,
    rating: Optional[int] = None,
    feedback: Optional[str] = None,
    key_takeaways: Optional[str] = None,
    current_user: dict = Depends(get_current_user)
):
    """Complete mentor connect session with feedback"""
    db = await get_database()
    
    try:
        session = await db["mentor_connects"].find_one({"_id": ObjectId(session_id)})
    except:
        raise HTTPException(status_code=400, detail="Invalid session ID")
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Verify user is the student (only students provide rating/feedback)
    if current_user["role"] != "student" or str(current_user["_id"]) != session["student_id"]:
        raise HTTPException(status_code=403, detail="Only session participants can complete")
    
    update_data = {
        "status": "completed",
        "completed_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    if rating is not None:
        update_data["session_rating"] = min(max(rating, 1), 5)  # 1-5 rating
    if feedback:
        update_data["session_feedback"] = feedback
    if key_takeaways:
        update_data["key_takeaways"] = [k.strip() for k in key_takeaways.split(';') if k.strip()]
    
    await db["mentor_connects"].update_one(
        {"_id": ObjectId(session_id)},
        {"$set": update_data}
    )
    
    # Make mentor available again
    await db["users"].update_one(
        {"_id": ObjectId(session["mentor_id"])},
        {"$set": {"available": True}}
    )
    
    # Award badges for successful session
    user = await db["users"].find_one({"_id": current_user["_id"]})
    badges_earned = []
    
    if rating and rating >= 4 and "Mentor Connected" not in user.get("badges", []):
        badges_earned.append("Mentor Connected")
    
    # Count successful mentor sessions
    successful_sessions = await db["mentor_connects"].count_documents({
        "student_id": str(current_user["_id"]),
        "status": "completed",
        "session_rating": {"$gte": 3}
    })
    
    if successful_sessions >= 3 and "Mentorship Master" not in user.get("badges", []):
        badges_earned.append("Mentorship Master")
    
    if badges_earned:
        await db["users"].update_one(
            {"_id": current_user["_id"]},
            {"$addToSet": {"badges": {"$each": badges_earned}}}
        )
    
    return {
        "message": "Session completed successfully",
        "badges_earned": badges_earned
    }

@router.get("/my-mentions")
async def get_my_mentor_connections(
    status_filter: Optional[str] = None,
    current_user: dict = Depends(get_current_user)
):
    """Get all mentor connections for current user"""
    db = await get_database()
    
    query = {
        "$or": [
            {"student_id": str(current_user["_id"])},
            {"mentor_id": str(current_user["_id"])}
        ]
    }
    
    if status_filter:
        query["status"] = status_filter
    
    connections = await db["mentor_connects"].find(query).sort("created_at", -1).limit(20).to_list(20)
    
    for conn in connections:
        conn["_id"] = str(conn["_id"])
        # Add user type for UI
        if str(current_user["_id"]) == conn["student_id"]:
            conn["my_role"] = "student"
        else:
            conn["my_role"] = "mentor"
    
    return connections

@router.get("/available-mentors")
async def get_available_mentors(
    current_user: dict = Depends(get_current_user)
):
    """Get list of available mentors for direct connect"""
    # Check if user qualifies
    user_badges = len(current_user.get("badges", []))
    if user_badges < 5:
        raise HTTPException(
            status_code=403,
            detail=".2f"
        )
    
    db = await get_database()
    
    mentors = await db["users"].find({
        "role": "mentor",
        "available": True
    }).to_list(10)
    
    # Add matching scores based on user's skills
    user_skills = set(current_user.get("skills", []) + current_user.get("domains", []))
    
    mentor_list = []
    for mentor in mentors:
        mentor_skills = set(mentor.get("expertise", []))
        match_score = len(user_skills & mentor_skills)
        
        mentor_list.append({
            "id": str(mentor["_id"]),
            "name": mentor["name"],
            "expertise": mentor.get("expertise", []),
            "experience_years": mentor.get("experience_years", 0),
            "match_score": match_score,
            "skills_overlap": list(user_skills & mentor_skills)
        })
    
    mentor_list.sort(key=lambda x: x["match_score"], reverse=True)
    
    return {
        "available_mentors": mentor_list[:5],  # Return top 5 matches
        "your_badges_count": user_badges,
        "required_badges": 5
    }

@router.get("/stats/mentorship")
async def get_mentorship_stats(
    current_user: dict = Depends(get_current_user)
):
    """Get comprehensive mentorship statistics"""
    db = await get_database()
    
    # Only for students
    if current_user["role"] != "student":
        raise HTTPException(status_code=403, detail="Only students have mentorship stats")
    
    completed_sessions = await db["mentor_connects"].count_documents({
        "student_id": str(current_user["_id"]),
        "status": "completed"
    })
    
    # Get ratings
    rated_sessions = await db["mentor_connects"].find({
        "student_id": str(current_user["_id"]),
        "status": "completed",
        "session_rating": {"$exists": True}
    }).to_list(None)
    
    avg_rating = 0
    if rated_sessions:
        total_rating = sum(session["session_rating"] for session in rated_sessions if session.get("session_rating"))
        avg_rating = total_rating / len([s for s in rated_sessions if s.get("session_rating")])
    
    return {
        "total_sessions": completed_sessions,
        "average_rating": round(avg_rating, 1) if avg_rating else 0,
        "mentors_connected": len(set(s["mentor_id"] for s in rated_sessions)),
        "badges_from_mentorship": len([b for b in current_user.get("badges", []) if "Mentor" in b])
    }

@router.get("/recommend/career-exploration")
async def get_career_exploration_recommendations(
    current_user: dict = Depends(get_current_user)
):
    """Get career exploration options (unlocked with apex badges)"""
    # This feature is unlocked only after earning apex badges
    
    user_badges = current_user.get("badges", [])
    apex_badges = ["Interview Ace", "Mentorship Master", "Career Explorer", "Industry Expert"]
    
    earned_apex = len(set(user_badges) & set(apex_badges))
    
    if earned_apex < len(apex_badges) // 2:  # Need at least half
        raise HTTPException(
            status_code=403,
            detail=f"This feature requires earning {len(apex_badges)//2} apex badges. Current: {earned_apex}"
        )
    
    db = await get_database()
    
    # Get unconventional career recommendations based on user profile
    user_interests = current_user.get("interests", [])
    user_skills = current_user.get("skills", [])
    
    # Query career paths from database (would be populated with actual career data)
    career_recommendations = await db["career_paths"].find({
        "tags": {"$in": user_interests + user_skills}
    }).limit(5).to_list(5)
    
    if not career_recommendations:
        # Fallback recommendations
        career_recommendations = [
            {
                "_id": "fallback_1",
                "career_title": "AI Ethics Consultant",
                "description": "Guide the ethical development and deployment of AI systems",
                "required_skills": ["AI", "Ethics", "Policy"],
                "growth_potential": "High",
                "salary_range": "$120K-$180K"
            },
            {
                "_id": "fallback_2",
                "career_title": "Sustainable Tech Innovator",
                "description": "Develop technology solutions for environmental challenges",
                "required_skills": ["Sustainability", "Innovation", "Tech"],
                "growth_potential": "Very High",
                "salary_range": "$100K-$160K"
            }
        ]
    
    return {
        "unconventional_careers": [
            {
                "id": str(c["_id"]),
                "title": c.get("career_title", c.get("title")),
                "description": c.get("description"),
                "required_skills": c.get("required_skills", []),
                "growth_potential": c.get("growth_potential", "Medium"),
                "salary_range": c.get("salary_range", "Varies"),
                "match_score": len(set(c.get("tags", [])) & set(user_interests + user_skills))
            }
            for c in career_recommendations
        ],
        "earned_apex_badges": earned_apex,
        "required_apex_badges": len(apex_badges)//2,
        "message": "Explore unconventional career paths tailored to your profile!"
    }
