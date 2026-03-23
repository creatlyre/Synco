from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.auth.dependencies import get_current_user
from app.database.database import get_db
from app.i18n import inject_template_i18n
from app.notifications.repository import NotificationRepository
from app.notifications.service import NotificationService
from app.users.repository import UserRepository

router = APIRouter(prefix="/notifications", tags=["notification-views"])
templates = Jinja2Templates(directory="app/templates")


def _service(db) -> NotificationService:
    return NotificationService(NotificationRepository(db), UserRepository(db))


@router.get("/badge", response_class=HTMLResponse)
async def notification_badge(request: Request, user=Depends(get_current_user), db=Depends(get_db)):
    svc = _service(db)
    count = svc.unread_count(user.id)
    if count > 0:
        display = str(count) if count <= 99 else "99+"
        return HTMLResponse(
            f'<span class="absolute -top-1 -right-1 flex h-5 w-5 items-center justify-center rounded-full bg-red-500 text-[10px] font-bold text-white">{display}</span>'
        )
    return HTMLResponse("")


@router.get("/dropdown", response_class=HTMLResponse)
async def notification_dropdown(request: Request, user=Depends(get_current_user), db=Depends(get_db)):
    svc = _service(db)
    notifications = svc.list_for_user(user.id)
    pref = svc.get_preference(user.id)
    context = inject_template_i18n(request, {
        "request": request,
        "notifications": notifications,
        "email_enabled": pref.email_enabled,
    })
    return templates.TemplateResponse("partials/notification_dropdown.html", context)


@router.post("/{notification_id}/read-html", response_class=HTMLResponse)
async def mark_read_html(notification_id: str, request: Request, user=Depends(get_current_user), db=Depends(get_db)):
    svc = _service(db)
    result = svc.mark_read(notification_id, user.id)
    if result:
        # Re-fetch to get actor_name
        actor = UserRepository(_service(db).user_repo.db).get_user_by_id(result.actor_user_id)
        actor_name = actor.name if actor else ""
        n = {
            "id": result.id,
            "type": result.type,
            "entity_title": result.entity_title,
            "is_read": True,
            "created_at": result.created_at,
            "actor_name": actor_name,
            "entity_type": result.entity_type,
        }
        context = inject_template_i18n(request, {"request": request, "n": n})
        return templates.TemplateResponse("partials/notification_item.html", context)
    return HTMLResponse("")


@router.post("/read-all-html", response_class=HTMLResponse)
async def mark_all_read_html(request: Request, user=Depends(get_current_user), db=Depends(get_db)):
    svc = _service(db)
    svc.mark_all_read(user.id)
    return await notification_dropdown(request=request, user=user, db=db)


@router.post("/{notification_id}/dismiss-html", response_class=HTMLResponse)
async def dismiss_html(notification_id: str, request: Request, user=Depends(get_current_user), db=Depends(get_db)):
    svc = _service(db)
    svc.dismiss(notification_id, user.id)
    return HTMLResponse("")


@router.put("/preferences-html", response_class=HTMLResponse)
async def toggle_email_pref(request: Request, user=Depends(get_current_user), db=Depends(get_db)):
    svc = _service(db)
    current = svc.get_preference(user.id)
    new_pref = svc.update_preference(user.id, not current.email_enabled)
    context = inject_template_i18n(request, {"request": request, "email_enabled": new_pref.email_enabled})
    checked = "checked" if new_pref.email_enabled else ""
    t = context["t"]
    return HTMLResponse(
        f'<label class="flex items-center gap-2 text-xs text-white/60 cursor-pointer">'
        f'<input type="checkbox" {checked} hx-put="/notifications/preferences-html" hx-target="#email-toggle-container" hx-swap="innerHTML" class="accent-indigo-500">'
        f'{t("notification.email_toggle_label")}</label>'
    )
