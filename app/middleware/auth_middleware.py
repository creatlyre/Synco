import jwt
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import RedirectResponse

from config import Settings


class SessionValidationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        public_routes = {
            "/health",
            "/auth/login",
            "/auth/callback",
            "/docs",
            "/openapi.json",
            "/redoc",
        }

        if request.url.path in public_routes or request.url.path.startswith("/static"):
            return await call_next(request)

        session_cookie = request.cookies.get("session")
        if not session_cookie:
            return RedirectResponse(url="/auth/login", status_code=307)

        settings = Settings()
        try:
            payload = jwt.decode(
                session_cookie,
                settings.SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM],
            )
            request.state.user_id = payload.get("user_id")
        except jwt.InvalidTokenError:
            return RedirectResponse(url="/auth/login", status_code=307)

        return await call_next(request)
