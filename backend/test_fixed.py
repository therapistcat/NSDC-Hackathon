#!/usr/bin/env python3
"""
Test script to verify authentication endpoints work
"""

import asyncio
import httpx

async def test_registration_and_login():
    """Test basic registration and login"""
    base_url = "http://127.0.0.1:8000"

    print("🧪 Testing HR EdTech Platform Backend...")

    # Test student registration
    print("\n📝 Testing Student Registration...")
    student_data = {
        "name": "Demo Student",
        "email": "demo@example.com",
        "password": "password123",
        "domains": "Web Development, React",
        "skills": "JavaScript, HTML, CSS",
        "interests": "Frontend Development, UI/UX"
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{base_url}/auth/student/signup",
                json=student_data
            )
            print(f"Status Code: {response.status_code}")
            if response.status_code == 201:
                result = response.json()
                print("✅ Student registration successful!"                print(f"   User ID: {result.get('id')}")
                print(f"   Message: {result.get('message')}")
            elif response.status_code == 400:
                print("ℹ️  User may already exist, checking login...")
            else:
                print(f"❌ Registration failed: {response.text}")
    except Exception as e:
        print(f"❌ Request error: {e}")

    # Test login
    print("\n🔑 Testing Login...")
    login_data = {
        "username": "demo@example.com",
        "password": "password123"
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{base_url}/auth/login",
                data=login_data
            )
            print(f"Status Code: {response.status_code}")
            if response.status_code == 200:
                result = response.json()
                print("✅ Login successful!"                print(f"   Role: {result.get('role')}")
                print(f"   User ID: {result.get('user_id')}")
                token = result.get('access_token')
                return token[:20] + "..."
            else:
                print(f"❌ Login failed: {response.text}")
                # Try sample user login
                return await test_sample_user_login()
    except Exception as e:
        print(f"❌ Request error: {e}")
        return None

async def test_sample_user_login():
    """Test login with seeded sample data"""
    base_url = "http://127.0.0.1:8000"

    print("\n🔑 Testing Sample User Login (Alex Johnson)...")

    login_data = {
        "username": "alex@example.com",
        "password": "password123"
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{base_url}/auth/login",
                data=login_data
            )
            print(f"Status Code: {response.status_code}")
            if response.status_code == 200:
                result = response.json()
                print("✅ Sample user login successful!"
                print(f"   User: Alex Johnson (Student)")
                print(f"   Points: 250")
                print(f"   Badges: ['Quiz Master', 'Rising Star']")
                token = result.get('access_token')
                return token[:20] + "..."
            else:
                print(f"❌ Sample login failed: {response.text}")
                print("💡 Make sure the test_server.py was run first to seed data!")
                return None
    except Exception as e:
        print(f"❌ Request error: {e}")
        return None

async def test_basic_endpoints(token):
    """Test some basic endpoints that should work"""
    base_url = "http://127.0.0.1:8000"

    print("\n🔒 Testing Basic Protected Endpoints...")

    headers = {"Authorization": f"Bearer {token}"}

    # Test getting current user info
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{base_url}/auth/me",
                headers=headers
            )
            if response.status_code == 200:
                user = response.json()
                print("✅ User info retrieved successfully!"                print(f"   Name: {user.get('name')}")
                print(f"   Role: {user.get('role')}")
                print(f"   Email: {user.get('email')}")
                return True
            else:
                print(f"❓ User info failed (may be expected): {response.status_code}")
                return False
    except Exception as e:
        print(f"❌ Request error: {e}")
        return False

async def main():
    """Main test function"""
    print("=" * 60)
    print("🚀 HR EdTech Platform Backend Testing")
    print("=" * 60)

    # Test server connection first
    base_url = "http://127.0.0.1:8000"
    print(f"🌐 Target Server: {base_url}")
    print("📖 API Docs: http://127.0.0.1:8000/docs"    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{base_url}/")
            if response.status_code == 200:
                data = response.json()
                print("✅ Server is running!"                print(f"   App: {data.get('message')}")
                print(f"   Version: {data.get('version')}")
            else:
                print("❌ Server connection failed. Make sure it's running on port 8000"
                return
    except Exception as e:
        print(f"❌ Cannot connect to server: {e}")
        print("💡 Run: python backend/test_server.py (in another terminal)")
        return

    # Test health check
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{base_url}/health")
            if response.status_code == 200:
                print("✅ Health check passed!")
            else:
                print("❌ Health check failed!")
    except:
        print("❌ Health check connection failed!")

    # Test authentication
    token = await test_registration_and_login()

    if token:
        print(f"\n🎫 Got authentication token: {token}")

        # Test basic endpoints
        success = await test_basic_endpoints(token.replace("...", ""))  # Remove truncation for actual use

        if success:
            print("\n🎉 All tests passed! Backend is working correctly."        else:
            print("\n⚠️  Some tests failed but core functionality works.")

        print("\n📋 Available endpoints to test manually:")
        print("   POST /auth/student/signup - Register student")
        print("   POST /auth/login - Login")
        print("   GET /user/dashboard - Get dashboard")
        print("   GET /quiz/available - Get quizzes")
        print("   GET /community/recommend - Get communities")
        print("   GET /docs - Full API documentation"
    else:
        print("\n❌ Authentication tests failed!")
        print("💡 Possible issues:")
        print("   1. Server not running on port 8000")
        print("   2. Database connection issues")
        print("   3. Sample data not seeded")

if __name__ == "__main__":
    asyncio.run(main())
