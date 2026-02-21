# ==========================================
# Include Routers
# ==========================================

from fastapi import APIRouter

from app.api.auth.router import router as auth_router
from app.api.utils.router import router as utils_router

app_router = APIRouter(
    
)
app_router.include_router(auth_router)
app_router.include_router(utils_router)