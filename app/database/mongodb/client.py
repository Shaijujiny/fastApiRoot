from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

from app.config import settings as CONFIG_SETTINGS
from app.core.logging.logger import get_logger


log = get_logger(__name__)
db_client: MongoClient = None  # type: ignore  # noqa: PGH003


class MongoDBSingleton:
    """Singleton class for MongoDB connection."""

    _instance = None
    _client: MongoClient | None = None

    def __new__(cls)-> "MongoDBSingleton":
        """Create and return a singleton instance."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            connection_string = CONFIG_SETTINGS.MONGODB_URI
            cls._instance._client = MongoClient(connection_string)
            log.info("Connected to MongoDB")
        return cls._instance

    def get_main_db(self) -> Database:
        db_name = CONFIG_SETTINGS.MONGODB_DB
        if self._client is None:
            msg = "MongoDB client is not initialized"
            raise RuntimeError(msg)
        return self._client[db_name]

    def get_collection(self, collection_name: str, index: str | None = None) -> Collection:
        """Get a collection from the main database."""
        db = self.get_main_db()
        if collection_name not in db.list_collection_names():
            db.create_collection(collection_name)
            # Create index if provided
            if index:
                db[collection_name].create_index(index, unique=True)
        return db[collection_name]
