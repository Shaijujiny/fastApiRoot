from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.api.products.schema import (
    ProductCreateRequest,
    ProductUpdateRequest,
)
from app.core.error.error_types import ErrorType
from app.core.error.message_codes import MessageCode
from app.core.response.response_builder import ResponseBuilder


class ProductService:
    COLLECTION_NAME = "products"

    @staticmethod
    async def create_product(
        db: AsyncIOMotorDatabase, data: ProductCreateRequest, user_id: int, lang: str
    ):
        product_dict = data.model_dump()
        product_dict["is_active"] = True
        product_dict["created_by"] = user_id

        result = await db[ProductService.COLLECTION_NAME].insert_one(product_dict)
        product_dict["id"] = str(result.inserted_id)
        product_dict.pop("_id", None)  # Remove non-serializable ObjectId

        return ResponseBuilder.build(
            ErrorType.SUC_201_RESOURCE_CREATED,
            MessageCode.RESOURCE_CREATED,
            lang,
            data=product_dict,
        )

    @staticmethod
    async def get_all_products(db: AsyncIOMotorDatabase, lang: str):
        cursor = db[ProductService.COLLECTION_NAME].find({"is_active": True})
        products = []
        async for doc in cursor:
            doc["id"] = str(doc.pop("_id"))
            products.append(doc)

        return ResponseBuilder.build(
            ErrorType.SUC_200_SUCCESS, MessageCode.DATA_FETCHED, lang, data=products
        )

    @staticmethod
    async def get_product_by_id(db: AsyncIOMotorDatabase, product_id: str, lang: str):
        if not ObjectId.is_valid(product_id):
            return ResponseBuilder.build(
                ErrorType.VAL_400_INVALID_INPUT, MessageCode.INVALID_INPUT, lang
            )

        doc = await db[ProductService.COLLECTION_NAME].find_one(
            {"_id": ObjectId(product_id), "is_active": True}
        )
        if not doc:
            return ResponseBuilder.build(
                ErrorType.RES_404_NOT_FOUND, MessageCode.RESOURCE_NOT_FOUND, lang
            )

        doc["id"] = str(doc.pop("_id"))
        return ResponseBuilder.build(
            ErrorType.SUC_200_SUCCESS, MessageCode.DATA_FETCHED, lang, data=doc
        )

    @staticmethod
    async def update_product(
        db: AsyncIOMotorDatabase, product_id: str, data: ProductUpdateRequest, lang: str
    ):
        if not ObjectId.is_valid(product_id):
            return ResponseBuilder.build(
                ErrorType.VAL_400_INVALID_INPUT, MessageCode.INVALID_INPUT, lang
            )

        update_data = {
            k: v
            for k, v in data.model_dump(exclude_unset=True).items()
            if v is not None
        }
        if not update_data:
            return ResponseBuilder.build(
                ErrorType.VAL_400_INVALID_INPUT, MessageCode.INVALID_INPUT, lang
            )

        result = await db[ProductService.COLLECTION_NAME].update_one(
            {"_id": ObjectId(product_id)}, {"$set": update_data}
        )

        if result.matched_count == 0:
            return ResponseBuilder.build(
                ErrorType.RES_404_NOT_FOUND, MessageCode.RESOURCE_NOT_FOUND, lang
            )

        doc = await db[ProductService.COLLECTION_NAME].find_one(
            {"_id": ObjectId(product_id)}
        )
        doc["id"] = str(doc.pop("_id"))

        return ResponseBuilder.build(
            ErrorType.SUC_200_SUCCESS, MessageCode.DATA_UPDATED, lang, data=doc
        )

    @staticmethod
    async def delete_product(db: AsyncIOMotorDatabase, product_id: str, lang: str):
        if not ObjectId.is_valid(product_id):
            return ResponseBuilder.build(
                ErrorType.VAL_400_INVALID_INPUT, MessageCode.INVALID_INPUT, lang
            )

        # Soft delete
        result = await db[ProductService.COLLECTION_NAME].update_one(
            {"_id": ObjectId(product_id)}, {"$set": {"is_active": False}}
        )

        if result.matched_count == 0:
            return ResponseBuilder.build(
                ErrorType.RES_404_NOT_FOUND, MessageCode.RESOURCE_NOT_FOUND, lang
            )

        return ResponseBuilder.build(
            ErrorType.SUC_200_SUCCESS, MessageCode.DATA_DELETED, lang
        )
