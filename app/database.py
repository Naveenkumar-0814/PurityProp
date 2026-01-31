from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine
from app.config import settings

# Create MongoDB client
client = AsyncIOMotorClient(settings.database_url)

# Create Odmantic engine
engine = AIOEngine(client=client, database=settings.database_name)

def get_engine():
    """Return the database engine."""
    return engine

def init_db():
    """No initialization needed for MongoDB (schemaless)."""
    # We could ensure indexes here if needed
    pass
