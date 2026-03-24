from __future__ import annotations

from fastapi import Depends, HTTPException, Request
from fastapi.responses import RedirectResponse

from app.auth.dependencies import get_current_user
from app.billing.repository import BillingRepository
from app.database.database import get_db


class UpgradeRedirect(Exception):
    """Raised when an HTML page requires a plan upgrade."""
    pass


async def get_current_plan(
    user=Depends(get_current_user),
    db=Depends(get_db),
) -> str:
    repo = BillingRepository(db)
    sub = repo.get_subscription(user.id)
    if sub:
        return sub.plan
    return "free"


def require_plan(*allowed_plans: str):
    async def _dependency(
        request: Request,
        user=Depends(get_current_user),
        db=Depends(get_db),
    ) -> str:
        repo = BillingRepository(db)
        sub = repo.get_subscription(user.id)
        plan = sub.plan if sub else "free"
        if plan not in allowed_plans:
            accept = request.headers.get("accept", "")
            if "text/html" in accept:
                raise UpgradeRedirect()
            raise HTTPException(
                status_code=403,
                detail="Upgrade required",
                headers={"X-Upgrade-URL": "/billing/settings"},
            )
        return plan

    return _dependency


def get_user_plan_for_template(user, db) -> str:
    repo = BillingRepository(db)
    sub = repo.get_subscription(user.id)
    return sub.plan if sub else "free"
