"""
Tests for PWA & Mobile Distribution (Phase 32).

Validates manifest, service worker, icons, offline page, base.html integration,
auth bypass for PWA routes, TWA config, and native deferral documentation.
"""
import json
import os


# ── MOB-01: Manifest Endpoint ──────────────────────────────────────────────


class TestManifestEndpoint:
    """GET /manifest.json returns correct Synco PWA metadata."""

    def test_manifest_returns_200(self, test_client):
        resp = test_client.get("/manifest.json")
        assert resp.status_code == 200

    def test_manifest_content_type(self, test_client):
        resp = test_client.get("/manifest.json")
        assert "manifest" in resp.headers["content-type"]

    def test_manifest_name(self, test_client):
        data = test_client.get("/manifest.json").json()
        assert data["name"] == "Synco"
        assert data["short_name"] == "Synco"

    def test_manifest_start_url(self, test_client):
        data = test_client.get("/manifest.json").json()
        assert data["start_url"] == "/dashboard"

    def test_manifest_display_standalone(self, test_client):
        data = test_client.get("/manifest.json").json()
        assert data["display"] == "standalone"

    def test_manifest_has_icons(self, test_client):
        data = test_client.get("/manifest.json").json()
        assert len(data["icons"]) >= 4
        sizes = {icon["sizes"] for icon in data["icons"]}
        assert "192x192" in sizes
        assert "512x512" in sizes

    def test_manifest_has_maskable_icon(self, test_client):
        data = test_client.get("/manifest.json").json()
        purposes = [icon.get("purpose", "") for icon in data["icons"]]
        assert any("maskable" in p for p in purposes)

    def test_manifest_theme_colors(self, test_client):
        data = test_client.get("/manifest.json").json()
        assert data["theme_color"] == "#1e1553"
        assert data["background_color"] == "#0f0a2e"


# ── MOB-01: Service Worker Endpoint ────────────────────────────────────────


class TestServiceWorkerEndpoint:
    """GET /sw.js returns service worker with correct headers."""

    def test_sw_returns_200(self, test_client):
        resp = test_client.get("/sw.js")
        assert resp.status_code == 200

    def test_sw_content_type(self, test_client):
        resp = test_client.get("/sw.js")
        assert "javascript" in resp.headers["content-type"]

    def test_sw_no_cache_header(self, test_client):
        resp = test_client.get("/sw.js")
        assert resp.headers.get("cache-control") == "no-cache"

    def test_sw_scope_header(self, test_client):
        resp = test_client.get("/sw.js")
        assert resp.headers.get("service-worker-allowed") == "/"

    def test_sw_has_install_handler(self, test_client):
        text = test_client.get("/sw.js").text
        assert "install" in text

    def test_sw_has_activate_handler(self, test_client):
        text = test_client.get("/sw.js").text
        assert "activate" in text

    def test_sw_has_fetch_handler(self, test_client):
        text = test_client.get("/sw.js").text
        assert "fetch" in text

    def test_sw_has_offline_fallback(self, test_client):
        text = test_client.get("/sw.js").text
        assert "offline" in text.lower()


# ── MOB-01: App Icons ──────────────────────────────────────────────────────


class TestAppIcons:
    """PWA icons are accessible via /static/icons/."""

    ICONS = [
        "icon-192.png",
        "icon-512.png",
        "icon-maskable-192.png",
        "icon-maskable-512.png",
    ]

    def test_icons_exist_on_disk(self):
        for icon in self.ICONS:
            path = os.path.join("public", "icons", icon)
            assert os.path.exists(path), f"Missing icon: {path}"
            assert os.path.getsize(path) > 100, f"Icon too small: {path}"

    def test_icons_served_via_static(self, test_client):
        for icon in self.ICONS:
            resp = test_client.get(f"/static/icons/{icon}")
            assert resp.status_code == 200, f"/static/icons/{icon} returned {resp.status_code}"


# ── MOB-01: Offline Page ───────────────────────────────────────────────────


class TestOfflinePage:
    """Branded offline fallback page exists and is self-contained."""

    def test_offline_html_exists(self):
        assert os.path.exists("public/offline.html")

    def test_offline_html_has_offline_message(self):
        content = open("public/offline.html", encoding="utf-8").read()
        assert "offline" in content.lower()

    def test_offline_html_has_synco_branding(self):
        content = open("public/offline.html", encoding="utf-8").read()
        assert "Synco" in content

    def test_offline_html_has_inline_css(self):
        content = open("public/offline.html", encoding="utf-8").read()
        assert "<style>" in content

    def test_offline_html_under_5kb(self):
        size = os.path.getsize("public/offline.html")
        assert size < 5120, f"offline.html is {size} bytes, expected < 5KB"


# ── MOB-01: base.html PWA Integration ──────────────────────────────────────


class TestBaseHtmlIntegration:
    """base.html includes manifest link, icons, SW registration, install prompt."""

    def _read_base(self):
        return open("app/templates/base.html", encoding="utf-8").read()

    def test_manifest_link(self):
        html = self._read_base()
        assert 'rel="manifest"' in html
        assert "/manifest.json" in html

    def test_apple_touch_icon(self):
        html = self._read_base()
        assert "apple-touch-icon" in html

    def test_service_worker_registration(self):
        html = self._read_base()
        assert "serviceWorker" in html
        assert "register" in html

    def test_install_prompt(self):
        html = self._read_base()
        assert "beforeinstallprompt" in html


# ── MOB-01: Auth Bypass for PWA Routes ─────────────────────────────────────


class TestPwaPublicRoutes:
    """PWA asset routes bypass session authentication."""

    def test_manifest_no_auth_redirect(self, test_client):
        resp = test_client.get("/manifest.json", follow_redirects=False)
        assert resp.status_code == 200

    def test_sw_no_auth_redirect(self, test_client):
        resp = test_client.get("/sw.js", follow_redirects=False)
        assert resp.status_code == 200


# ── MOB-02: TWA Configuration ──────────────────────────────────────────────


class TestTwaConfig:
    """android/twa-config.json is valid and has correct Synco metadata."""

    def test_twa_config_exists(self):
        assert os.path.exists("android/twa-config.json")

    def test_twa_config_valid_json(self):
        with open("android/twa-config.json") as f:
            data = json.load(f)
        assert isinstance(data, dict)

    def test_twa_config_metadata(self):
        with open("android/twa-config.json") as f:
            data = json.load(f)
        assert data["name"] == "Synco"
        assert data["startUrl"] == "/dashboard"
        assert data["packageId"] == "app.synco.twa"
        assert data["display"] == "standalone"

    def test_twa_config_host(self):
        with open("android/twa-config.json") as f:
            data = json.load(f)
        assert "host" in data
        assert data["host"]  # non-empty

    def test_android_readme_exists(self):
        assert os.path.exists("android/README.md")
        content = open("android/README.md", encoding="utf-8").read()
        assert len(content) > 500
        assert "bubblewrap" in content.lower() or "Bubblewrap" in content


# ── MOB-03: Native Deferral Documentation ──────────────────────────────────


class TestNativeDeferral:
    """MONETIZATION.md documents mobile strategy and native app deferral."""

    def _read_monetization(self):
        return open("MONETIZATION.md", encoding="utf-8").read()

    def test_mobile_strategy_section(self):
        content = self._read_monetization()
        assert "Mobile Access Strategy" in content

    def test_pwa_mentioned(self):
        content = self._read_monetization()
        assert "PWA" in content

    def test_twa_mentioned(self):
        content = self._read_monetization()
        assert "TWA" in content or "Trusted Web Activity" in content

    def test_native_deferral_explicit(self):
        content = self._read_monetization()
        assert "deferred" in content.lower()
