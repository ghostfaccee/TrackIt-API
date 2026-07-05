import traceback

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from app.core.database import engine, Base
from app.core.middleware import LoggingMiddleware
from app.api import router
from app.core.logger import logger

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        logger.info('Application started')
    yield

app = FastAPI(lifespan = lifespan)

@app.exception_handler(Exception)
async def global_exeption_handler(request: Request, exc: Exception):
    logger.error(
        f'Unhandled error on {request.method} {request.url.path}\n'
        f'{traceback.format_exc()}'
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal Server Error."}
    )

app.add_middleware(LoggingMiddleware)
app.include_router(router)