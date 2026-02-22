from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorCollection,
    AsyncIOMotorDatabase,
)

from app.config import settings as CONFIG_SETTINGS
from app.core.logging.logger import get_logger

log = get_logger(__name__)


class MongoDBSingleton:
    """Singleton class for MongoDB connection using Motor (Async)."""

    _instance = None
    _client: AsyncIOMotorClient | None = None

    def __new__(cls) -> "MongoDBSingleton":
        """Create and return a singleton instance."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            connection_string = CONFIG_SETTINGS.MONGODB_URI
            cls._instance._client = AsyncIOMotorClient(connection_string)
            log.info("Connected to MongoDB (Async)")
        return cls._instance

    def get_main_db(self) -> AsyncIOMotorDatabase:
        db_name = CONFIG_SETTINGS.MONGODB_DB
        if self._client is None:
            msg = "MongoDB client is not initialized"
            raise RuntimeError(msg)
        return self._client[db_name]

    async def get_collection(
        self, collection_name: str, index: str | None = None
    ) -> AsyncIOMotorCollection:
        """Get a collection from the main database."""
        db = self.get_main_db()
        # Motor's list_collection_names is a coroutine
        cols = await db.list_collection_names()
        if collection_name not in cols:
            await db.create_collection(collection_name)
            if index:
                await db[collection_name].create_index(index, unique=True)
        return db[collection_name]
