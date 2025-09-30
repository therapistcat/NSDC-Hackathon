#!/usr/bin/env python3
"""
Test script to verify authentication endpoints work
"""

import asyncio
import httpx
import json

async def test_auth_endpoints():
    """Test registration and login endpoints"""
    base_url = "http://127.0.0.1:8000"

    print("🧪 Testing Authentication Endpoints...")

    # Test student registration
    print("\n📝 Testing Student Registration...")
    student_data = {
        "name": "Test Student",
        "email": "test@example.com",
        "password": "password123",
        "domains": "Web Development, JavaScript",
        "skills": "React, HTML, CSS",
        "interests": "Frontend Development, UI/UX"
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{base_url}/auth/student/signup",
                json=student_data
            )
            print(f"Status: {response.status_code}")
            if response.status_code == 201:
                print("✅ Student registration successful!")
                result = response.json()
                print(f"   User ID: {result.get('id')}")
            else:
                print(f"❌ Student registration failed: {response.text}")
    except Exception as e:
        print(f"❌ Request error: {e}")

    # Test mentor registration
    print("\n📝 Testing Mentor Registration...")
    mentor_data = {
        "name": "Test Mentor",
        "email": "mentor@example.com",
        "password": "password123",
        "expertise": "Data Science, Python, Machine Learning",
        "experience_years": 8
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{base_url}/auth/mentor/signup",
                json=mentor_data
            )
            print(f"Status: {response.status_code}")
            if response.status_code == 201:
                print("✅ Mentor registration successful!")
                result = response.json()
                print(f"   User ID: {result.get('id')}")
            else:
                print(f"❌ Mentor registration failed: {response.text}")
    except Exception as e:
        print(f"❌ Request error: {e}")

    # Test login
    print("\n🔑 Testing Login...")
    login_data = {
        "username": "test@example.com",
        "password": "password123"
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{base_url}/auth/login",
                data=login_data
            )
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                print("✅ Login successful!")
                result = response.json()
                token = result.get('access_token')
                role = result.get('role')
                print(f"   Token: {token[:20]}...")
                print(f"   Role: {role}")
                return token
            else:
                print(f"❌ Login failed: {response.text}")
                return None
    except Exception as e:
        print(f"❌ Request error: {e}")
        return None

async def test_protected_endpoints(token):
    """Test endpoints that require authentication"""
    base_url = "http://127.0.0.1:8000"
    headers = {"Authorization": f"Bearer {token}"}

    print("
🔒 Testing Protected Endpoints..."    # Test dashboard
    print("\n📊 Testing Dashboard...")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{base_url}/user/dashboard",
                headers=headers
            )
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                print("✅ Dashboard access successful!")
                result = response.json()
                print(f"   User role: {result.get('user_profile', {}).get('role')}")
                print(f"   Points: {result.get('user_profile', {}).get('points')}")
                print(f"   Badges: {result.get('gamification', {}).get('earned_badges')}")
            else:
                print(f"❌ Dashboard access failed: {response.text}")
    except Exception as e:
        print(f"❌ Request error: {e}")

    # Test quiz availability
    print("\n🎮 Testing Quiz Availability...")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{base_url}/quiz/available",
                headers=headers
            )
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                print("✅ Quiz list access successful!")
                result = response.json()
                print(f"   Available quizzes: {len(result)}")
                if result:
                    print(f"   First quiz: {result[0].get('title')}")
            else:
                print(f"❌ Quiz list access failed: {response.text}")
    except Exception as e:
        print(f"❌ Request error: {e}")

    # Test community recommendations
    print("\n👥 Testing Community Recommendations...")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{base_url}/community/recommend",
                headers=headers
            )
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                print("✅ Community recommendations successful!")
                result = response.json()
                print(f"   Communities: {result.get('total_results', 0)}")
            else:
                print(f"❌ Community recommendations failed: {response.text}")
    except Exception as e:
        print(f"❌ Request error: {e}")

async def test_sample_login():
    """Test login with sample data"""
    base_url = "http://127.0.0.1:8000"

    print("\n🔑 Testing Sample User Login (from seeded data)...")
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
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                print("✅ Sample user login successful!")
                result = response.json()
                token = result.get('access_token')
                print(f"   User role: {result.get('role')}")
                return token
            else:
                print(f"❌ Sample user login failed: {response.text}")
                return None
    except Exception as e:
        print(f"❌ Request error: {e}")
        return None

async def main():
    """Main test function"""
    print("🚀 Testing HR EdTech Backend Auth & API Endpoints")

    # Test registration endpoints
    token = await test_auth_endpoints()

    if token:
        # Test protected endpoints
        await test_protected_endpoints(token)

    # Test sample data login
    sample_token = await test_sample_login()
    if sample_token:
        await test_protected_endpoints(sample_token)

    print("\n🎉 Testing complete!")

if __name__ == "__main__":
    asyncio.run(main())
