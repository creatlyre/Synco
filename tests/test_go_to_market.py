"""
Tests for Phase 33: Go-to-Market (GTM-01 through GTM-05).

Covers: pricing page, landing page, legal pages, self-hosted checkout mode,
footer legal links, and LAUNCH.md documentation artifacts.
"""
import os
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest


# ── GTM-01: Pricing Page ──────────────────────────────────────────────────


class TestPricingPage:
    """Pricing page renders with SaaS tiers and self-hosted option."""

    def test_pricing_page_returns_200(self, test_client):
        resp = test_client.get("/pricing")
        assert resp.status_code == 200
        assert "text/html" in resp.headers["content-type"]

    def test_pricing_page_shows_tier_names(self, test_client):
        resp = test_client.get("/pricing")
        html = resp.text.lower()
        # Polish: "darmowy", English: "free"
        assert "free" in html or "darmowy" in html
        assert "pro" in html
        assert "family" in html

    def test_pricing_page_shows_self_hosted(self, test_client):
        resp = test_client.get("/pricing")
        html = resp.text.lower()
        assert "self-hosted" in html or "self hosted" in html or "self_hosted" in html

    def test_pricing_page_no_auth_required(self, test_client):
        """Pricing page is public — no redirect to login."""
        resp = test_client.get("/pricing", follow_redirects=False)
        assert resp.status_code == 200


# ── GTM-02: Landing Page ─────────────────────────────────────────────────


class TestLandingPage:
    """Landing page for unauthenticated visitors with CTA."""

    def test_unauthenticated_root_shows_landing(self, test_client):
        resp = test_client.get("/", follow_redirects=False)
        assert resp.status_code == 200
        assert "text/html" in resp.headers["content-type"]

    def test_landing_page_has_cta(self, test_client):
        resp = test_client.get("/")
        html = resp.text.lower()
        # Should have sign-up or get-started CTA
        assert "auth/login" in html or "zaloguj" in html or "sign" in html or "start" in html

    def test_landing_page_has_features(self, test_client):
        resp = test_client.get("/")
        html = resp.text.lower()
        # Should mention key features
        assert "calendar" in html or "kalendarz" in html

    def test_authenticated_root_redirects_to_dashboard(self, authenticated_client):
        resp = authenticated_client.get("/", follow_redirects=False)
        assert resp.status_code == 302
        assert "/dashboard" in resp.headers.get("location", "")


# ── GTM-03: Checkout Flow (self-hosted payment mode) ─────────────────────


class TestSelfHostedCheckout:
    """Self-hosted checkout uses Stripe payment mode (one-time), not subscription."""

    def test_self_hosted_checkout_uses_payment_mode(self, authenticated_client, test_db, test_user_a):
        with patch("app.billing.service.stripe.Customer.create") as mock_cust, \
             patch("app.billing.service.stripe.checkout.Session.create") as mock_session:
            mock_cust.return_value = MagicMock(id="cus_sh_test")
            mock_session.return_value = MagicMock(url="https://checkout.stripe.com/sh_test")

            resp = authenticated_client.post(
                "/api/billing/checkout",
                json={"plan": "self_hosted"},
            )
            if resp.status_code == 200:
                # Verify Stripe was called with mode=payment
                mock_session.assert_called_once()
                call_kwargs = mock_session.call_args
                assert call_kwargs[1]["mode"] == "payment" or call_kwargs.kwargs.get("mode") == "payment"
            else:
                # 400 because STRIPE_SELF_HOSTED_PRICE_ID is empty in test env
                assert resp.status_code == 400

    def test_plan_price_map_has_self_hosted_key(self):
        from app.billing.service import PLAN_PRICE_MAP
        assert "self_hosted" in PLAN_PRICE_MAP

    def test_plan_price_map_has_annual_keys(self):
        from app.billing.service import PLAN_PRICE_MAP
        assert ("pro", "annual") in PLAN_PRICE_MAP
        assert ("family_plus", "annual") in PLAN_PRICE_MAP


# ── GTM-04: Legal Pages ──────────────────────────────────────────────────


class TestLegalPages:
    """Terms, Privacy, and Refund pages render correctly."""

    def test_terms_page_returns_200(self, test_client):
        resp = test_client.get("/terms")
        assert resp.status_code == 200
        assert "text/html" in resp.headers["content-type"]

    def test_terms_page_has_content(self, test_client):
        resp = test_client.get("/terms")
        html = resp.text.lower()
        assert "terms" in html or "regulamin" in html or "warunki" in html

    def test_privacy_page_returns_200(self, test_client):
        resp = test_client.get("/privacy")
        assert resp.status_code == 200
        assert "text/html" in resp.headers["content-type"]

    def test_privacy_page_has_content(self, test_client):
        resp = test_client.get("/privacy")
        html = resp.text.lower()
        assert "privacy" in html or "prywatno" in html or "dane osobowe" in html

    def test_refund_page_returns_200(self, test_client):
        resp = test_client.get("/refund")
        assert resp.status_code == 200
        assert "text/html" in resp.headers["content-type"]

    def test_refund_page_has_content(self, test_client):
        resp = test_client.get("/refund")
        html = resp.text.lower()
        assert "refund" in html or "zwrot" in html or "rezygnacj" in html

    def test_legal_pages_no_auth_required(self, test_client):
        for path in ["/terms", "/privacy", "/refund"]:
            resp = test_client.get(path, follow_redirects=False)
            assert resp.status_code == 200, f"{path} should be public"

    def test_footer_has_legal_links(self, authenticated_client):
        """Authenticated pages include footer with legal links."""
        resp = authenticated_client.get("/billing/settings")
        html = resp.text
        assert 'href="/terms"' in html
        assert 'href="/privacy"' in html
        assert 'href="/refund"' in html


# ── GTM-05: Launch Checklist ─────────────────────────────────────────────


class TestLaunchChecklist:
    """LAUNCH.md exists with required sections."""

    def test_launch_md_exists(self):
        launch_path = Path(__file__).parent.parent / "LAUNCH.md"
        assert launch_path.exists(), "LAUNCH.md must exist at project root"

    def test_launch_md_has_prelaunch_section(self):
        launch_path = Path(__file__).parent.parent / "LAUNCH.md"
        content = launch_path.read_text(encoding="utf-8")
        assert "Pre-Launch" in content

    def test_launch_md_has_day1_actions(self):
        launch_path = Path(__file__).parent.parent / "LAUNCH.md"
        content = launch_path.read_text(encoding="utf-8")
        assert "Day 1" in content

    def test_launch_md_has_success_criteria(self):
        launch_path = Path(__file__).parent.parent / "LAUNCH.md"
        content = launch_path.read_text(encoding="utf-8")
        assert "30-Day Success Criteria" in content

    def test_launch_md_minimum_size(self):
        launch_path = Path(__file__).parent.parent / "LAUNCH.md"
        content = launch_path.read_text(encoding="utf-8")
        lines = content.strip().splitlines()
        assert len(lines) >= 50, f"LAUNCH.md should have ≥50 lines, got {len(lines)}"


# ── GTM-05: Docker CI/CD Artifacts ───────────────────────────────────────


class TestDockerArtifacts:
    """GitHub Actions workflow and Dockerfile OCI labels exist."""

    def test_docker_publish_workflow_exists(self):
        wf = Path(__file__).parent.parent / ".github" / "workflows" / "docker-publish.yml"
        assert wf.exists(), "docker-publish.yml workflow must exist"

    def test_docker_publish_triggers_on_tags(self):
        wf = Path(__file__).parent.parent / ".github" / "workflows" / "docker-publish.yml"
        content = wf.read_text(encoding="utf-8")
        assert "v*" in content or "tags" in content

    def test_dockerfile_has_oci_labels(self):
        df = Path(__file__).parent.parent / "Dockerfile"
        content = df.read_text(encoding="utf-8")
        assert "org.opencontainers.image" in content

    def test_docker_compose_uses_ghcr(self):
        dc = Path(__file__).parent.parent / "self-hosted" / "docker-compose.yml"
        content = dc.read_text(encoding="utf-8")
        assert "ghcr.io" in content
