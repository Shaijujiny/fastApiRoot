from typing import Optional

from app.core.response.base_schema import CustomModel


class ProductCreateRequest(CustomModel):
    name: str
    description: str
    price: float
    category: str


class ProductUpdateRequest(CustomModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None


class ProductResponse(CustomModel):
    id: str
    name: str
    description: str
    price: float
    category: str
    is_active: bool
    created_by: int
