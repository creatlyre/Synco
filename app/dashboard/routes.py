from typing import Optional

from fastapi import APIRouter, Cookie, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.auth.dependencies import get_current_user
from app.dashboard.service import DashboardService
from app.database.database import get_db
from app.i18n import inject_template_i18n, set_locale_cookie_if_param

router = APIRouter(prefix="/dashboard", tags=["dashboard"])
templates = Jinja2Templates(directory="app/templates")


@router.get("", response_class=HTMLResponse)
async def dashboard_page(
    request: Request,
    user=Depends(get_current_user),
    db=Depends(get_db),
    session: Optional[str] = Cookie(None),
):
    service = DashboardService(db, auth_token=session)

    all_today = service.get_today_events(user.calendar_id, user.id)
    today_events = all_today[:5]
    today_overflow = max(0, len(all_today) - 5)

    week_preview = service.get_week_preview(user.calendar_id, user.id)
    category_map = service.get_event_categories(user.calendar_id)
    budget_snapshot = service.get_budget_snapshot(user.calendar_id)
    top_categories = service.get_top_expense_categories(user.calendar_id)

    from datetime import datetime

    context = inject_template_i18n(
        request,
        {
            "request": request,
            "user": user,
            "now": datetime.utcnow(),
            "today_events": today_events,
            "today_overflow": today_overflow,
            "week_preview": week_preview,
            "category_map": category_map,
            "budget_snapshot": budget_snapshot,
            "top_categories": top_categories,
        },
    )

    response = templates.TemplateResponse(
        request=request, name="dashboard.html", context=context,
    )
    set_locale_cookie_if_param(response, request)
    return response
