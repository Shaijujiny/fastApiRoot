from typing import List, Optional

import strawberry
from strawberry.types import Info

from app.graphql.context import GraphQLContext


@strawberry.type
class UserType:
    id: int
    username: str
    email: str
    role: str
    is_active: bool


@strawberry.type
class ProductType:
    id: str
    name: str
    description: str
    price: float
    category: str


@strawberry.type
class Query:
    @strawberry.field
    async def me(self, info: Info[GraphQLContext, None]) -> Optional[UserType]:
        user = await info.context.get_user()
        if not user:
            return None
        return UserType(
            id=user.id,
            username=user.username,
            email=user.email,
            role=user.role,
            is_active=user.is_active,
        )

    @strawberry.field
    async def products(self, info: Info[GraphQLContext, None]) -> List[ProductType]:
        from app.database.mongodb.client import MongoDBSingleton

        db = MongoDBSingleton().get_main_db()
        cursor = db["products"].find({"is_active": True})

        products = []
        async for doc in cursor:
            products.append(
                ProductType(
                    id=str(doc["_id"]),
                    name=doc["name"],
                    description=doc["description"],
                    price=doc["price"],
                    category=doc["category"],
                )
            )
        return products


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_product(
        self,
        info: Info[GraphQLContext, None],
        name: str,
        description: str,
        price: float,
        category: str,
    ) -> ProductType:
        user = await info.context.get_user()
        if not user:
            raise Exception("Unauthorized")

        from app.database.mongodb.client import MongoDBSingleton

        db = MongoDBSingleton().get_main_db()

        product_dict = {
            "name": name,
            "description": description,
            "price": price,
            "category": category,
            "is_active": True,
        }

        result = await db["products"].insert_one(product_dict)
        return ProductType(
            id=str(result.inserted_id),
            name=name,
            description=description,
            price=price,
            category=category,
        )


schema = strawberry.Schema(query=Query, mutation=Mutation)
