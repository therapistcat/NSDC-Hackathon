from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from datetime import datetime, timedelta
from bson import ObjectId
from app.db.database import get_database
from app.api.routers.auth import get_current_user

router = APIRouter(prefix="/learning", tags=["AI-Powered Micro Learning"])

@router.get("/daily-content")
async def get_daily_content(
    current_user: dict = Depends(get_current_user)
):
    """Get AI-curated daily micro-learning content with flashcards"""
    db = await get_database()
    
    user_tags = current_user.get("tags", [])
    user_domains = current_user.get("domains", [])
    user_skills = current_user.get("skills", [])
    user_interests = current_user.get("interests", [])
    
    # Combine all user preferences for content curation
    all_tags = set(user_tags + user_domains + user_skills + user_interests)
    
    # Get content based on user profile
    content_query = []
    if all_tags:
        # Find content matching user's tags (via regex match on tags)
        tag_regex_patterns = [{"tags": {"$regex": tag, "$options": "i"}} for tag in list(all_tags)]
        content_query = {"$or": tag_regex_patterns}
    
    # Get daily content (simulation - in real implementation, use AI/ML to predict)
    contents = await db["learning_content"].find(content_query).limit(5).to_list(5)
    
    if not contents:
        # Fallback: get popular content if no matches
        contents = await db["learning_content"].find().sort("views", -1).limit(5).to_list(5)
    
    # Convert ObjectId to string and add flashcard structure
    for content in contents:
        content["_id"] = str(content["_id"])
        # Generate flashcards from content (simulation)
        content["flashcards"] = generate_flashcards(content)
    
    return {
        "daily_content": contents,
        "total_items": len(contents),
        "message": "AI-curated learning content for today"
    }

def generate_flashcards(content: dict) -> List[dict]:
    """Generate flashcards from learning content (simulation)"""
    content_text = content.get("content", "")
    title = content.get("title", "")
    
    # In real implementation, use NLP to extract key points
    flashcards = [
        {
            "question": f"What is {title.lower()}?",
            "answer": content.get("summary", "Learning content description").strip()[:200],
            "topic": content.get("topic", "General"),
            "difficulty": "easy"
        },
        {
            "question": f"Key concepts in {title.lower()}",
            "answer": ", ".join(content.get("key_concepts", ["Main concepts", "Secondary concepts"])),
            "topic": content.get("topic", "General"),
            "difficulty": "medium"
        },
        {
            "question": f"How to apply {title.lower()}?",
            "answer": content.get("application_tips", "Practical applications of this concept"),
            "topic": content.get("topic", "General"),
            "difficulty": "hard"
        }
    ]
    
    return flashcards

@router.post("/content/{content_id}/view")
async def mark_content_viewed(
    content_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Mark content as viewed and update progress"""
    db = await get_database()
    
    # Check if content exists
    try:
        content = await db["learning_content"].find_one({"_id": ObjectId(content_id)})
    except:
        raise HTTPException(status_code=400, detail="Invalid content ID")
    
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    
    # Update view count
    await db["learning_content"].update_one(
        {"_id": ObjectId(content_id)},
        {"$inc": {"views": 1}}
    )
    
    # Record user progress
    await db["learning_progress"].insert_one({
        "user_id": str(current_user["_id"]),
        "content_id": content_id,
        "viewed_at": datetime.utcnow(),
        "time_spent": 0,  # Would be tracked in real implementation
        "completed": True
    })
    
    return {"message": "Content marked as viewed"}

@router.get("/resources")
async def get_learning_resources(
    topic: Optional[str] = None,
    skill_level: Optional[str] = None,
    current_user: dict = Depends(get_current_user)
):
    """Get detailed learning resources (videos, articles, etc.)"""
    db = await get_database()
    
    query = {}
    if topic:
        query["topic"] = {"$regex": topic, "$options": "i"}
    if skill_level:
        query["skill_level"] = skill_level
    
    resources = await db["learning_resources"].find(query).limit(20).to_list(20)
    
    for resource in resources:
        resource["_id"] = str(resource["_id"])
        # Add match score based on user interests
        user_interests = current_user.get("interests", [])
        resource_tags = resource.get("tags", [])
        overlap = len(set(user_interests) & set(resource_tags))
        resource["match_score"] = overlap
    
    # Sort by relevance (match score)
    resources.sort(key=lambda x: x.get("match_score", 0), reverse=True)
    
    return {
        "resources": resources,
        "total_found": len(resources),
        "message": f"Learning resources for {topic or 'general topics'}"
    }

@router.post("/roadmap")
async def create_personal_learning_roadmap(
    career_goal: str,
    time_commitment: str,  # days_per_week
    current_level: str,   # beginner/intermediate/advanced
    current_user: dict = Depends(get_current_user)
):
    """Generate AI-powered personalized learning roadmap"""
    db = await get_database()
    
    # In real implementation, this would use ML to create personalized roadmap
    # For now, simulate based on user profile
    
    user_skills = current_user.get("skills", [])
    user_domains = current_user.get("domains", [])
    
    roadmap_stages = [
        {
            "stage": 1,
            "title": f"Foundation in {', '.join(user_domains[:2])}",
            "duration": "2-3 weeks",
            "milestones": ["Complete basics", "Build first projects"],
            "recommended_resources": await get_recommended_resources(user_domains[:2], current_level)
        },
        {
            "stage": 2,
            "title": f"Advanced {career_goal} Skills",
            "duration": "4-6 weeks",
            "milestones": ["Master intermediate concepts", "Build portfolio project"],
            "recommended_resources": await get_recommended_resources([career_goal], current_level)
        },
        {
            "stage": 3,
            "title": "Specialization and Practice",
            "duration": "6-8 weeks",
            "milestones": ["Focus on weak areas", "Mock interviews", "Networking"],
            "recommended_resources": []
        }
    ]
    
    # Save roadmap to database
    roadmap_data = {
        "user_id": str(current_user["_id"]),
        "career_goal": career_goal,
        "time_commitment": time_commitment,
        "current_level": current_level,
        "stages": roadmap_stages,
        "created_at": datetime.utcnow(),
        "progress": {
            "current_stage": 1,
            "completed_milestones": [],
            "completion_percentage": 0
        }
    }
    
    result = await db["learning_roadmaps"].insert_one(roadmap_data)
    
    return {
        "roadmap_id": str(result.inserted_id),
        "roadmap": roadmap_stages,
        "message": f"Personalized learning roadmap created for {career_goal}"
    }

async def get_recommended_resources(domains: List[str], skill_level: str) -> List[dict]:
    """Helper function to get recommended resources"""
    db = await get_database()
    
    # Simple resource recommendation (real implementation would use ML)
    resources = []
    for domain in domains:
        resource_list = await db["learning_resources"].find({
            "topic": {"$regex": domain, "$options": "i"},
            "skill_level": skill_level
        }).limit(3).to_list(3)
        
        for resource in resource_list:
            resources.append({
                "id": str(resource["_id"]),
                "title": resource["title"],
                "type": resource.get("resource_type", "article"),
                "url": resource.get("url", "#")
            })
    
    return resources[:5]

@router.get("/progress/streak")
async def get_learning_streak(
    current_user: dict = Depends(get_current_user)
):
    """Get user's daily learning streak"""
    db = await get_database()
    
    # Get all learning progress for current user (last 30 days)
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    
    progress_count = await db["learning_progress"].count_documents({
        "user_id": str(current_user["_id"]),
        "viewed_at": {"$gte": thirty_days_ago}
    })
    
    # Calculate streak (simplified - assumes daily activity)
    streak_days = min(progress_count, 30)  # Max 30 days for display
    
    return {
        "current_streak": streak_days,
        "days_active_this_month": progress_count,
        "total_content_viewed": progress_count,
        "message": f"You're on a {streak_days} day learning streak!"
    }

@router.get("/trends")
async def get_learning_trends(
    current_user: dict = Depends(get_current_user)
):
    """Get personalized learning trend insights"""
    db = await get_database()
    
    # Get content consumption patterns (last 7 days)
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    
    recent_progress = await db["learning_progress"].find({
        "user_id": str(current_user["_id"]),
        "viewed_at": {"$gte": seven_days_ago}
    }).to_list(50)
    
    # Analyze trends (simplified)
    topics_viewed = {}
    for progress in recent_progress:
        content = await db["learning_content"].find_one({"_id": ObjectId(progress["content_id"])})
        if content:
            topic = content.get("topic", "General")
            topics_viewed[topic] = topics_viewed.get(topic, 0) + 1
    
    top_topics = sorted(topics_viewed.items(), key=lambda x: x[1], reverse=True)[:3]
    
    return {
        "top_topics_this_week": top_topics,
        "total_content_viewed": len(recent_progress),
        "insights": [
            "You prefer video content over articles",
            "Morning (9-11 AM) is your most productive time",
            f"Your interest in {top_topics[0][0] if top_topics else 'technical topics'} is growing"
        ]
    }
