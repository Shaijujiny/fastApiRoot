from typing import Optional

from pydantic import Field

from app.core.response.base_schema import CustomModel


class ProductMongoModel(CustomModel):
    id: Optional[str] = Field(None, alias="_id")
    name: str
    description: str
    price: float
    category: str
    is_active: bool = True
