from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routers import auth, quiz, community, interview, learning, user, mentor_interviews
from app.db.database import connect_to_mongo, close_mongo_connection

app = FastAPI(
    title="HR EdTech Platform for Gen Z",
    description="""
    Interactive HR learning platform tailored for Gen Z with gamification, micro-learning,
    community features, and AI-powered mentorship.
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware for frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "*"],  # Add your frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_db_client():
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_db_client():
    await close_mongo_connection()

@app.get("/")
async def root():
    return {
        "message": "HR EdTech Platform API",
        "version": "1.0.0",
        "features": [
            "Gamified Quiz System with Reinforcement Learning",
            "AI-Powered Micro Learning",
            "Community Hub with Semantic Search",
            "Mock Interview Scheduling",
            "Direct Mentor Connections",
            "Career Exploration Tools"
        ]
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}

# Include all routers
app.include_router(auth.router, prefix="/api/v1", tags=["Authentication"])
app.include_router(user.router, prefix="/api/v1", tags=["User Management"])
app.include_router(quiz.router, prefix="/api/v1", tags=["Quiz & Gamification"])
app.include_router(learning.router, prefix="/api/v1", tags=["Micro Learning"])
app.include_router(community.router, prefix="/api/v1", tags=["Community Hub"])
app.include_router(interview.router, prefix="/api/v1", tags=["Mock Interviews"])
app.include_router(mentor_interviews.router, prefix="/api/v1", tags=["Mentor Connect"])
