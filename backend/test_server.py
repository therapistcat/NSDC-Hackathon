#!/usr/bin/env python3
"""
Test script to run the FastAPI server and add sample data
"""

import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

async def test_imports():
    """Test all imports to find issues"""
    try:
        from main import app
        print("✅ Main app import successful")

        from app.db.database import connect_to_mongo, get_database, close_mongo_connection
        print("✅ Database imports successful")

        from app.api.routers.auth import router as auth_router
        print("✅ Auth router import successful")

        from app.api.routers.quiz import router as quiz_router
        print("✅ Quiz router import successful")

        from app.api.routers.user import router as user_router
        print("✅ User router import successful")

        from app.api.routers.community import router as community_router
        print("✅ Community router import successful")

        from app.api.routers.interview import router as interview_router
        print("✅ Interview router import successful")

        from app.api.routers.learning import router as learning_router
        print("✅ Learning router import successful")

        from app.api.routers.mentor_interviews import router as mentor_router
        print("✅ Mentor router import successful")

        print("\n🎉 All imports successful! Ready to run server.")
        return True

    except Exception as e:
        print(f"❌ Import error: {e}")

        # Try to connect to MongoDB gracefully
        try:
            await connect_to_mongo()
            print("✅ MongoDB connection successful")
        except Exception as db_error:
            print(f"⚠️  MongoDB connection failed: {db_error}")
            print("     Server will run without database functionality")
        return False

async def add_sample_data():
    """Add sample users, quizzes, and content for testing"""
    try:
        from app.db.database import get_database, connect_to_mongo
        from datetime import datetime
        from passlib.context import CryptContext

        await connect_to_mongo()
        db = await get_database()
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

        print("\n📥 Adding sample data...")

        # Sample Student
        hashed_password = pwd_context.hash("password123")
        student_data = {
            "name": "Alex Johnson",
            "email": "alex@example.com",
            "password": hashed_password,
            "role": "student",
            "tags": ["python", "data science", "machine learning"],
            "domains": ["Data Science", "AI"],
            "skills": ["Python", "SQL", "Machine Learning"],
            "interests": ["AI", "Data Science", "Career Development"],
            "points": 250,
            "badges": ["Quiz Master", "Rising Star"],
            "streak": 7,
            "quiz_attempts": [],
            "mock_interviews": [],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }

        # Check if student exists
        existing_student = await db["users"].find_one({"email": "alex@example.com"})
        if not existing_student:
            result = await db["users"].insert_one(student_data)
            print(f"✅ Sample student created: {result.inserted_id}")
        else:
            print("📝 Sample student already exists")

        # Sample Mentor
        mentor_data = {
            "name": "Dr. Sarah Chen",
            "email": "sarah@mentor.com",
            "password": pwd_context.hash("password123"),
            "role": "mentor",
            "expertise": ["Data Science", "Machine Learning", "Python"],
            "experience_years": 12,
            "available": True,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }

        existing_mentor = await db["users"].find_one({"email": "sarah@mentor.com"})
        if not existing_mentor:
            result = await db["users"].insert_one(mentor_data)
            print(f"✅ Sample mentor created: {result.inserted_id}")
        else:
            print("📝 Sample mentor already exists")

        # Sample Quiz
        quiz_data = {
            "title": "Python Fundamentals",
            "difficulty": "easy",
            "questions": [
                {
                    "question": "What is the correct way to declare a variable in Python?",
                    "options": ["var x = 5", "x := 5", "x = 5", "let x = 5"],
                    "correct_answer": "x = 5"
                },
                {
                    "question": "Which of these is NOT a Python data type?",
                    "options": ["list", "tuple", "array", "dict"],
                    "correct_answer": "array"
                }
            ],
            "points": 10,
            "time_limit": 300,
            "created_by": "system",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }

        existing_quiz = await db["quizzes"].find_one({"title": "Python Fundamentals"})
        if not existing_quiz:
            result = await db["quizzes"].insert_one(quiz_data)
            print(f"✅ Sample quiz created: {result.inserted_id}")
        else:
            print("📝 Sample quiz already exists")

        # Sample Community
        community_data = {
            "name": "Data Science Learners",
            "description": "Community for aspiring data scientists",
            "topic": "Data Science",
            "tags": ["data science", "machine learning", "python"],
            "members": [],
            "posts": [
                {
                    "title": "Welcome to our community!",
                    "content": "Let's learn data science together!",
                    "author_id": "system",
                    "author_name": "Community Admin",
                    "likes": 5,
                    "comments": [],
                    "created_at": datetime.utcnow()
                }
            ],
            "created_by": "system",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }

        existing_community = await db["communities"].find_one({"name": "Data Science Learners"})
        if not existing_community:
            result = await db["communities"].insert_one(community_data)
            print(f"✅ Sample community created: {result.inserted_id}")
        else:
            print("📝 Sample community already exists")

        print("🎉 Sample data added successfully!")

    except Exception as e:
        print(f"❌ Error adding sample data: {e}")

async def run_server():
    """Run the FastAPI server"""
    import uvicorn

    print("🚀 Starting FastAPI server...")
    print("📍 API Docs: http://127.0.0.1:8001/docs")
    print("🏠 Root: http://127.0.0.1:8001")

    try:
        config = uvicorn.Config(
            "main:app",
            host="127.0.0.1",
            port=8001,
            reload=True,
            log_level="info"
        )
        server = uvicorn.Server(config)
        await server.serve()
    except Exception as e:
        print(f"❌ Server error: {e}")

async def main():
    """Main function"""
    print("🧪 Testing HR EdTech Platform Backend...")

    # Test imports
    imports_ok = await test_imports()

    if imports_ok:
        # Add sample data
        await add_sample_data()

        # Run server
        await run_server()
    else:
        print("❌ Tests failed. Please check the errors above.")

if __name__ == "__main__":
    asyncio.run(main())
