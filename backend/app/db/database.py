from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

class MongoDB:
    client: AsyncIOMotorClient = None
    db = None

async def get_database():
    """Returns the database instance"""
    return MongoDB.db

async def connect_to_mongo():
    """Connect to MongoDB"""
    MongoDB.client = AsyncIOMotorClient(settings.MONGODB_URL)
    MongoDB.db = MongoDB.client[settings.DATABASE_NAME]
    print(f"Connected to MongoDB: {settings.DATABASE_NAME}")
    
async def close_mongo_connection():
    """Close MongoDB connection"""
    if MongoDB.client:
        MongoDB.client.close()
        print("MongoDB connection closed")
