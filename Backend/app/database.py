from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine
from app.config import settings

_client = None
_engine = None

def get_engine() -> AIOEngine:
    global _client, _engine

    if _engine is None:
        _client = AsyncIOMotorClient(settings.database_url)
        _engine = AIOEngine(
            client=_client,
            database=settings.database_name
        )

    return _engine
