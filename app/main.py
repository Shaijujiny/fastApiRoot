from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.core.middleware.exception_middleware import AppException, app_exception_handler, global_exception_handler
from app.core.middleware.logging_middleware import LoggingMiddleware

from app.database.mongodb.client import MongoDBSingleton
from app.api import app_router


# ==========================================
# Create FastAPI App
# ==========================================

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.API_VERSION,
    description=settings.DESCRIPTION,
    docs_url="/docs" if settings.IS_SWAGGER_ENABLED else None,
    redoc_url="/redoc" if settings.IS_SWAGGER_ENABLED else None,
    openapi_url="/openapi.json" if settings.IS_SWAGGER_ENABLED else None,
    debug=settings.FASTAPI_DEBUG,
    root_path=settings.ROOT_PATH,
)


# ==========================================
# CORS Middleware
# ==========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================
# Custom Middleware
# ==========================================

app.add_middleware(LoggingMiddleware)


# ==========================================
# Exception Handler
# ==========================================

@app.exception_handler(AppException)
async def custom_exception_handler(request: Request, exc: AppException):
    return await app_exception_handler(request, exc)
app.add_exception_handler(Exception, global_exception_handler)


# ==========================================
# Startup / Shutdown Events
# ==========================================

@app.on_event("startup")
async def startup_event():
    """
    Initialize connections here
    """
    # MongoDB Connect
    _ = MongoDBSingleton()

    print("Application started successfully 🚀")


@app.on_event("shutdown")
async def shutdown_event():
    print("Application shutting down...")


# ==========================================
# Include Routers
# ==========================================

app.include_router(app_router)

    
# ==========================================
# Health Check Route
# ==========================================

@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "environment": settings.ENVIRONMENT
    }