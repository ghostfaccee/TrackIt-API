from fastapi import APIRouter
from app.api.v1.endpoints.habits import router as router_habits
from app.api.v1.endpoints.stats import router as router_stats
from app.api.v1.endpoints.log import router as router_log
from app.api.v1.endpoints.auth import router as router_auth

router = APIRouter()

@router.get('/', summary = 'Main page', description = 'Well, yes, the main page in api, what did you expect :))')
async def main_page():
    return {'Welcome to': 'the main page'}
router.include_router(router_habits)
router.include_router(router_stats)
router.include_router(router_log)
router.include_router(router_auth)