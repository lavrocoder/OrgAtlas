from fastapi import Depends, FastAPI

from app.admin import setup_admin
from app.api.routes.activities import router as activities_router
from app.api.routes.buildings import router as buildings_router
from app.api.routes.organizations import router as organizations_router
from app.core.config import settings
from app.core.security import verify_api_key

app = FastAPI(
    title="OrgAtlas API",
    description="REST API для справочника организаций, зданий и видов деятельности",
    version="1.0.0",
    dependencies=[Depends(verify_api_key)],
)

app.include_router(activities_router, prefix="/api/v1")
app.include_router(buildings_router, prefix="/api/v1")
app.include_router(organizations_router, prefix="/api/v1")

# Админ-панель (без API-ключа)
if settings.ENABLE_ADMIN:
    setup_admin(app)