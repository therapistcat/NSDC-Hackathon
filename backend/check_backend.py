#!/usr/bin/env python3
"""
Simple script to check if backend is running and working
"""

import requests
import json

def test_backend():
    """Test backend basic functionality"""
    base_url = "http://127.0.0.1:8000"

    print("=" * 60)
    print("🚀 HR EdTech Platform Backend Check")
    print("=" * 60)

    # Test server health
    print("🌐 Testing server connection...")
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            data = response.json()
            print("✅ Server is running!")
            print(f"   Message: {data.get('message')}")
            print(f"   Version: {data.get('version')}")
        else:
            print(f"❌ Server responded with status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to server: {e}")
        print("💡 Start the server with: python backend/main.py")
        print("   Or run: python backend/test_server.py")
        return False

    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("✅ Health check passed!")
        else:
            print("⚠️  Health check failed!")
    except:
        print("⚠️  Health check connection failed!")

    # Check API docs endpoint to see if routes are registered
    print("\n📚 Checking API documentation...")
    try:
        response = requests.get(f"{base_url}/docs")
        if response.status_code == 200:
            print("✅ API docs available at: http://127.0.0.1:8000/docs")
        else:
            print("⚠️  API docs not accessible")
    except:
        print("⚠️  API docs check failed")

    # Test student registration (using correct API prefix)
    print("\n📝 Testing Student Registration...")
    api_base = f"{base_url}/api/v1"
    student_data = {
        "name": "Test Student",
        "email": "test@example.com",
        "password": "password123",
        "domains": "Web Development, JavaScript",
        "skills": "React, HTML, CSS",
        "interests": "Frontend Development, UI/UX"
    }

    try:
        response = requests.post(
            f"{api_base}/auth/student/signup",
            json=student_data
        )
        print(f"Status Code: {response.status_code}")
        if response.status_code == 201:
            result = response.json()
            print("✅ Registration successful!")
            print(f"   User ID: {result.get('id')}")
            print(f"   Message: {result.get('message')}")
            return True
        elif response.status_code == 400:
            error_data = response.json()
            if "already registered" in error_data.get("detail", "").lower():
                print("ℹ️  User already exists (this is expected)")
                return True
            else:
                print(f"❌ Registration failed: {error_data}")
                return False
        else:
            print(f"❌ Unexpected response: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Registration request failed: {e}")
        print("💡 This usually means the server is running but has issues")
        return False

if __name__ == "__main__":
    success = test_backend()

    if success:
        print("\n🎉 Backend is working correctly!")
        print("\n📋 Next steps to fully test:")
        print("1. Visit API docs: http://127.0.0.1:8000/docs")
        print("2. Test authentication endpoints")
        print("3. Check dashboard and quiz endpoints")
        print("4. Test community and interview features")
        print("\n📱 Ready to build the frontend now!")
    else:
        print("\n❌ Backend needs fixes. Check the error messages above.")
        print("💡 Common issues:")
        print("   - MongoDB not running")
        print("   - Port 8000 in use")
        print("   - Dependencies missing")
