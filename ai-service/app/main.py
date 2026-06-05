from fastapi import FastAPI
from app.config import settings
from app.routers import health, classification

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.include_router(health.router, prefix="/api/v1", tags=["health"])
app.include_router(classification.router, prefix="/api/v1", tags=["classification"])


@app.get("/")
async def root():
    return {"service": settings.app_name, "version": settings.app_version}