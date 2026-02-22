from pymongo.database import Database

from app.database.mongodb.client import MongoDBSingleton


def get_mongo_db() -> Database:
    """Dependency for getting a MongoDB database connection."""
    return MongoDBSingleton().get_main_db()
