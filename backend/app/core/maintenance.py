from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.config import settings

class MaintenanceMiddleware(BaseHTTPMiddleware):
    """
    Checks if system is in maintenance mode.
    Exempts: /health, /docs, /redoc, /openapi.json, and /api/v1/admin routes.
    """
    async def dispatch(self, request: Request, call_next):
        # Path exemption
        path = request.url.path
        if (
            path.startswith("/health")
            or path.startswith("/docs")
            or path.startswith("/redoc")
            or path.startswith("/openapi.json")
            or path.startswith("/api/v1/admin")
            or path.startswith("/api/v1/auth/login")
            or not settings.MAINTENANCE_MODE
        ):
            return await call_next(request)

        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "detail": "System is currently undergoing planned maintenance. Please check back shortly.",
                "maintenance": True
            }
        )
