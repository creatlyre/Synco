from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Optional

from app.database.models import Subscription, BillingEvent
from app.database.supabase_store import SupabaseStore


def _parse_dt(value: str | None) -> datetime | None:
    if not value:
        return None
    if value.endswith("Z"):
        value = value.replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(value)
        if parsed.tzinfo is not None:
            return parsed.astimezone(timezone.utc).replace(tzinfo=None)
        return parsed
    except ValueError:
        return None


def _to_subscription(row: dict[str, Any]) -> Subscription:
    return Subscription(
        id=row.get("id", ""),
        user_id=row.get("user_id", ""),
        stripe_customer_id=row.get("stripe_customer_id"),
        stripe_subscription_id=row.get("stripe_subscription_id"),
        plan=row.get("plan", "free"),
        status=row.get("status", "active"),
        current_period_end=_parse_dt(row.get("current_period_end")),
        cancel_at_period_end=bool(row.get("cancel_at_period_end", False)),
        created_at=_parse_dt(row.get("created_at")),
        updated_at=_parse_dt(row.get("updated_at")),
    )


def _to_billing_event(row: dict[str, Any]) -> BillingEvent:
    return BillingEvent(
        id=row.get("id", ""),
        user_id=row.get("user_id", ""),
        event_type=row.get("event_type", ""),
        plan=row.get("plan"),
        stripe_event_id=row.get("stripe_event_id"),
        metadata=row.get("metadata") or {},
        created_at=_parse_dt(row.get("created_at")),
    )


class BillingRepository:
    def __init__(self, db: SupabaseStore):
        self.db = db

    def get_subscription(self, user_id: str) -> Optional[Subscription]:
        rows = self.db.select("subscriptions", {"user_id": f"eq.{user_id}"})
        if not rows:
            return None
        return _to_subscription(rows[0])

    def get_subscription_by_stripe_customer(self, stripe_customer_id: str) -> Optional[Subscription]:
        rows = self.db.select("subscriptions", {"stripe_customer_id": f"eq.{stripe_customer_id}"})
        if not rows:
            return None
        return _to_subscription(rows[0])

    def upsert_subscription(
        self,
        user_id: str,
        stripe_customer_id: str | None = None,
        stripe_subscription_id: str | None = None,
        plan: str = "free",
        status: str = "active",
        current_period_end: datetime | None = None,
        cancel_at_period_end: bool = False,
    ) -> Subscription:
        existing = self.get_subscription(user_id)
        payload: dict[str, Any] = {
            "plan": plan,
            "status": status,
            "cancel_at_period_end": cancel_at_period_end,
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }
        if stripe_customer_id is not None:
            payload["stripe_customer_id"] = stripe_customer_id
        if stripe_subscription_id is not None:
            payload["stripe_subscription_id"] = stripe_subscription_id
        if current_period_end is not None:
            payload["current_period_end"] = current_period_end.isoformat()

        if existing:
            row = self.db.update(
                "subscriptions",
                {"user_id": f"eq.{user_id}"},
                payload,
            )
            return _to_subscription(row) if row else existing
        else:
            payload["user_id"] = user_id
            row = self.db.insert("subscriptions", payload)
            return _to_subscription(row)

    def log_billing_event(
        self,
        user_id: str,
        event_type: str,
        plan: str | None = None,
        stripe_event_id: str | None = None,
        metadata: dict | None = None,
    ) -> BillingEvent:
        payload: dict[str, Any] = {
            "user_id": user_id,
            "event_type": event_type,
        }
        if plan is not None:
            payload["plan"] = plan
        if stripe_event_id is not None:
            payload["stripe_event_id"] = stripe_event_id
        if metadata:
            payload["metadata"] = metadata
        row = self.db.insert("billing_events", payload)
        return _to_billing_event(row)
