import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        print(f"Request from {request.headers.get("user-agent")} of length {request.headers.get("content-length")} started.")
        response = await call_next(request)
        print(f"Request from {request.headers.get("user-agent")} completed in {request.headers.get("X-Process-Time"):} seconds. Finished processing at {time.process_time()}")
        return response