from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response, JSONResponse
import os

class VerifyAuthenticationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        bearer_token = request.headers.get("Authorization")
        if bearer_token != "Bearer " + os.getenv("BEARER_TOKEN"):
            return JSONResponse(status_code=401, content={"detail": "Unauthorized"})
        return await call_next(request)