from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.api.products.schema import ProductCreateRequest, ProductUpdateRequest
from app.api.products.service import ProductService
from app.depends.jwt_depends import get_current_user
from app.depends.language_depends import get_language
from app.depends.mongo_depends import get_mongo_db

router = APIRouter(prefix="/products", tags=["Products (MongoDB)"])


@router.post("")
async def create_product(
    data: ProductCreateRequest,
    current_user=Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_mongo_db),
    lang: str = Depends(get_language),
):
    return await ProductService.create_product(db, data, current_user.id, lang)


@router.get("")
async def get_all_products(
    db: AsyncIOMotorDatabase = Depends(get_mongo_db), lang: str = Depends(get_language)
):
    return await ProductService.get_all_products(db, lang)


@router.get("/{product_id}")
async def get_product(
    product_id: str,
    db: AsyncIOMotorDatabase = Depends(get_mongo_db),
    lang: str = Depends(get_language),
):
    return await ProductService.get_product_by_id(db, product_id, lang)


@router.put("/{product_id}")
async def update_product(
    product_id: str,
    data: ProductUpdateRequest,
    current_user=Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_mongo_db),
    lang: str = Depends(get_language),
):
    # Pass current_user if needed for permission check
    return await ProductService.update_product(db, product_id, data, lang)


@router.delete("/{product_id}")
async def delete_product(
    product_id: str,
    current_user=Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_mongo_db),
    lang: str = Depends(get_language),
):
    return await ProductService.delete_product(db, product_id, lang)
