import os

from fastapi import Depends, FastAPI, Request
from fastapi.exceptions import HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.exc import SQLAlchemyError

from app.auth.dependencies import get_current_user
from app.auth.routes import router as auth_router
from app.database.database import Base, engine
from app.middleware.auth_middleware import SessionValidationMiddleware
from app.users.routes import router as users_router

# Initialize database schema. Use Alembic migrations for production evolution.
try:
    Base.metadata.create_all(bind=engine)
except SQLAlchemyError:
    # Allow app boot without hard-failing when DATABASE_URL is not configured yet.
    pass

app = FastAPI(
    title="CalendarPlanner",
    description="Shared household calendar with Google Calendar sync",
    version="1.0.0",
    debug=os.getenv("DEBUG", "false").lower() == "true",
)

templates = Jinja2Templates(directory="app/templates")

app.add_middleware(SessionValidationMiddleware)
app.include_router(auth_router)
app.include_router(users_router)


@app.get("/", response_class=HTMLResponse)
async def root(request: Request, user=Depends(get_current_user)):
    return templates.TemplateResponse(
        "calendar.html",
        {
            "request": request,
            "user": user,
        },
    )


@app.get("/invite", response_class=HTMLResponse)
async def invite_page(request: Request, user=Depends(get_current_user)):
    return templates.TemplateResponse(
        "invite.html",
        {
            "request": request,
            "user": user,
        },
    )


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.exception_handler(HTTPException)
async def auth_redirect_handler(request: Request, exc: HTTPException):
    if exc.status_code == 401 and request.url.path in {"/", "/invite"}:
        from fastapi.responses import RedirectResponse

        return RedirectResponse(url="/auth/login", status_code=307)
    raise exc


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=os.getenv("DEBUG", "false").lower() == "true",
    )
