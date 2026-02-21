from motor.motor_asyncio import AsyncIOMotorDatabase
from app.database.mongodb.client import MongoDBSingleton


async def get_mongo_db() -> AsyncIOMotorDatabase:
    return MongoDBSingleton().get_main_db(
        
    )