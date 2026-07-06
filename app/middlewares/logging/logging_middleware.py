import time
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.logger import logger
from app.core.config import settings


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start_time = time.time()
        logger.info(f'-> {request.method} {request.url.path}')
        try:
            response = await call_next(request)
            process_time = time.time() - start_time

            if process_time > settings.SLOW_REQUEST_THRESHOLD:
                logger.warning(
                    f"SLOW REQUEST: {request.method} {request.url.path} - "
                    f"Took {process_time:.2f}s (threshold: {settings.SLOW_REQUEST_THRESHOLD}s)"
                )
            else:
                logger.info(
                    f'<- {request.method} {request.url.path} - '
                    f'Status: {response.status_code} - '
                    f'Process time: {process_time:.2f}s'
                )
                return response
        except Exception as e:
            logger.error(f'{request.method} {request.url.path} - Error: {str(e)}')
            raise