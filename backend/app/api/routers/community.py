from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from datetime import datetime
from bson import ObjectId
from app.db.database import get_database
from app.api.routers.auth import get_current_user

router = APIRouter(prefix="/community", tags=["Community Hub"])

@router.post("/create")
async def create_community(
    name: str,
    description: str,
    topic: str,
    tags: str,
    current_user: dict = Depends(get_current_user)
):
    """Create a new community hub"""
    db = await get_database()
    
    community_data = {
        "name": name,
        "description": description,
        "topic": topic,
        "tags": [tag.strip() for tag in tags.split(',')],
        "members": [str(current_user["_id"])],
        "created_by": str(current_user["_id"]),
        "posts": [],
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    result = await db["communities"].insert_one(community_data)
    
    return {
        "id": str(result.inserted_id),
        "name": name,
        "message": "Community created successfully"
    }

@router.get("/recommend")
async def recommend_communities(
    current_user: dict = Depends(get_current_user)
):
    """Recommend communities based on user tags using semantic search"""
    db = await get_database()
    
    user_tags = current_user.get("tags", [])
    user_domains = current_user.get("domains", [])
    user_skills = current_user.get("skills", [])
    user_interests = current_user.get("interests", [])
    
    # Combine all user preferences
    all_user_tags = set(user_tags + user_domains + user_skills + user_interests)
    
    if not all_user_tags:
        # Return popular communities if no tags
        communities = await db["communities"].find().sort("members", -1).limit(10).to_list(10)
    else:
        # Find communities with matching tags (semantic search simulation)
        communities = await db["communities"].find().to_list(100)
        
        # Score communities based on tag overlap
        scored_communities = []
        for community in communities:
            community_tags = set(community.get("tags", []))
            overlap = len(all_user_tags & community_tags)
            if overlap > 0:
                community["match_score"] = overlap
                scored_communities.append(community)
        
        # Sort by match score
        scored_communities.sort(key=lambda x: x.get("match_score", 0), reverse=True)
        communities = scored_communities[:10]
    
    result = []
    for community in communities:
        result.append({
            "id": str(community["_id"]),
            "name": community["name"],
            "description": community["description"],
            "topic": community["topic"],
            "tags": community.get("tags", []),
            "members_count": len(community.get("members", [])),
            "match_score": community.get("match_score", 0)
        })
    
    return result

@router.get("/all")
async def get_all_communities(
    topic: Optional[str] = None,
    search: Optional[str] = None
):
    """Get all communities with optional filtering"""
    db = await get_database()
    
    query = {}
    if topic:
        query["topic"] = topic
    if search:
        query["$or"] = [
            {"name": {"$regex": search, "$options": "i"}},
            {"description": {"$regex": search, "$options": "i"}}
        ]
    
    communities = await db["communities"].find(query).to_list(100)
    
    result = []
    for community in communities:
        result.append({
            "id": str(community["_id"]),
            "name": community["name"],
            "description": community["description"],
            "topic": community["topic"],
            "tags": community.get("tags", []),
            "members_count": len(community.get("members", []))
        })
    
    return result

@router.post("/{community_id}/join")
async def join_community(
    community_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Join a community"""
    db = await get_database()
    
    try:
        community = await db["communities"].find_one({"_id": ObjectId(community_id)})
    except:
        raise HTTPException(status_code=400, detail="Invalid community ID")
    
    if not community:
        raise HTTPException(status_code=404, detail="Community not found")
    
    user_id = str(current_user["_id"])
    if user_id in community.get("members", []):
        raise HTTPException(status_code=400, detail="Already a member")
    
    await db["communities"].update_one(
        {"_id": ObjectId(community_id)},
        {
            "$addToSet": {"members": user_id},
            "$set": {"updated_at": datetime.utcnow()}
        }
    )
    
    return {"message": "Successfully joined community"}

@router.post("/{community_id}/leave")
async def leave_community(
    community_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Leave a community"""
    db = await get_database()
    
    try:
        community = await db["communities"].find_one({"_id": ObjectId(community_id)})
    except:
        raise HTTPException(status_code=400, detail="Invalid community ID")
    
    if not community:
        raise HTTPException(status_code=404, detail="Community not found")
    
    user_id = str(current_user["_id"])
    
    await db["communities"].update_one(
        {"_id": ObjectId(community_id)},
        {
            "$pull": {"members": user_id},
            "$set": {"updated_at": datetime.utcnow()}
        }
    )
    
    return {"message": "Successfully left community"}

@router.get("/{community_id}")
async def get_community_details(community_id: str):
    """Get community details including posts"""
    db = await get_database()
    
    try:
        community = await db["communities"].find_one({"_id": ObjectId(community_id)})
    except:
        raise HTTPException(status_code=400, detail="Invalid community ID")
    
    if not community:
        raise HTTPException(status_code=404, detail="Community not found")
    
    community["_id"] = str(community["_id"])
    community["members_count"] = len(community.get("members", []))
    
    return community

@router.post("/{community_id}/post")
async def create_post(
    community_id: str,
    title: str,
    content: str,
    current_user: dict = Depends(get_current_user)
):
    """Create a post in a community"""
    db = await get_database()
    
    try:
        community = await db["communities"].find_one({"_id": ObjectId(community_id)})
    except:
        raise HTTPException(status_code=400, detail="Invalid community ID")
    
    if not community:
        raise HTTPException(status_code=404, detail="Community not found")
    
    user_id = str(current_user["_id"])
    if user_id not in community.get("members", []):
        raise HTTPException(status_code=403, detail="Must be a member to post")
    
    post_data = {
        "title": title,
        "content": content,
        "author_id": user_id,
        "author_name": current_user["name"],
        "likes": 0,
        "comments": [],
        "created_at": datetime.utcnow()
    }
    
    await db["communities"].update_one(
        {"_id": ObjectId(community_id)},
        {
            "$push": {"posts": post_data},
            "$set": {"updated_at": datetime.utcnow()}
        }
    )
    
    return {"message": "Post created successfully"}

@router.get("/{community_id}/posts")
async def get_community_posts(community_id: str, limit: int = 50):
    """Get posts from a community"""
    db = await get_database()
    
    try:
        community = await db["communities"].find_one({"_id": ObjectId(community_id)})
    except:
        raise HTTPException(status_code=400, detail="Invalid community ID")
    
    if not community:
        raise HTTPException(status_code=404, detail="Community not found")
    
    posts = community.get("posts", [])
    posts.reverse()  # Most recent first
    
    return posts[:limit]
