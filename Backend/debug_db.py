import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

async def check_connection():
    try:
        print(f"Connecting to {settings.database_url}...")
        client = AsyncIOMotorClient(settings.database_url, serverSelectionTimeoutMS=5000)
        # Force connection
        await client.server_info()
        print("✅ MongoDB connection successful!")
        
        db = client[settings.database_name]
        collections = await db.list_collection_names()
        print(f"Collections: {collections}")
        
    except Exception as e:
        print(f"❌ MongoDB Connection Failed: {e}")

if __name__ == "__main__":
    asyncio.run(check_connection())
