# Synco Android Distribution (TWA)

Synco uses a **Trusted Web Activity (TWA)** to wrap the PWA in a native Android shell.
No custom Java/Kotlin code — Chrome renders the full app in standalone mode (no URL bar).

## Prerequisites

- Node.js 18+
- Java JDK 11+
- Android SDK (via Android Studio or standalone SDK tools)
- A deployed Synco instance with HTTPS and valid manifest at `/manifest.json`

## Quick Path: PWABuilder

The fastest way to generate an Android package:

1. Visit [pwabuilder.com](https://www.pwabuilder.com/)
2. Enter your Synco URL (e.g., `https://synco.app`)
3. Click **Start** — PWABuilder reads your manifest and service worker
4. Select **Android** → **Generate**
5. Download the generated APK/AAB
6. Configure Digital Asset Links (see below)

This produces a ready-to-upload AAB without any local tooling.

## CLI Path: Bubblewrap

For full control over the build process:

### 1. Install Bubblewrap

```bash
npm install -g @nicolo-ribaudo/nicolo-ribaudo--bubblewrap-cli
```

### 2. Initialize from Manifest

```bash
cd android/
bubblewrap init --manifest https://synco.app/manifest.json
```

Bubblewrap reads the manifest and generates an Android project.
Review the generated `twa-manifest.json` — compare with `twa-config.json` in this directory.

### 3. Build APK (for testing)

```bash
bubblewrap build
```

Produces `app-release-signed.apk` in the output directory.

### 4. Build AAB (for Play Store)

```bash
bubblewrap build --buildType=aab
```

Produces `app-release-bundle.aab` for Google Play upload.

### 5. Signing Key

On first build, Bubblewrap creates a signing keystore. **Back up this keystore** — you need it for all future updates.

```bash
# Extract SHA-256 fingerprint for Digital Asset Links
keytool -list -v -keystore synco-keystore.jks -alias synco
```

Copy the `SHA256:` fingerprint value for the next step.

## Digital Asset Links

To verify app-to-site ownership (eliminates the Chrome URL bar), serve a JSON file at:

```
https://synco.app/.well-known/assetlinks.json
```

Contents:

```json
[{
  "relation": ["delegate_permission/common.handle_all_urls"],
  "target": {
    "namespace": "android_app",
    "package_name": "app.synco.twa",
    "sha256_cert_fingerprints": ["YOUR_SHA256_FINGERPRINT_HERE"]
  }
}]
```

Replace `YOUR_SHA256_FINGERPRINT_HERE` with the SHA-256 extracted from keytool.

### Serving assetlinks.json

Add a route in `main.py` (similar to the manifest/sw.js routes):

```python
@app.get("/.well-known/assetlinks.json", include_in_schema=False)
async def asset_links():
    return FileResponse("public/.well-known/assetlinks.json",
                        media_type="application/json")
```

Create `public/.well-known/assetlinks.json` with your fingerprint.

## Testing

### Install on Device

```bash
adb install app-release-signed.apk
```

### Verify

- App opens in fullscreen (no URL bar) — confirms Digital Asset Links work
- Offline page shows when airplane mode is on
- Install prompt does not appear inside the TWA (already installed)
- Navigation works: calendar, budget, shopping, dashboard

### Emulator

```bash
# Start emulator
emulator -avd Pixel_6_API_33
# Install and test
adb install app-release-signed.apk
adb shell am start -n app.synco.twa/.LauncherActivity
```

## Requirements

| Requirement | Minimum |
|-------------|---------|
| Android version | 7.0 (API 24) |
| Chrome version | 72+ |
| Protocol | HTTPS required |
| Manifest | Must be valid at /manifest.json |

## Play Store Upload

> **Note:** Play Store listing is Phase 33 (Go-to-Market) scope.

High-level steps:

1. Create a Google Play Developer account ($25 one-time fee)
2. Create a new app in Play Console
3. Upload the AAB from `bubblewrap build --buildType=aab`
4. Fill in store listing (screenshots, description, category: Productivity)
5. Set up Digital Asset Links verification
6. Submit for review

## Configuration Reference

See `twa-config.json` in this directory for the Bubblewrap configuration values.
Key fields:

| Field | Value | Notes |
|-------|-------|-------|
| `host` | synco.app | Production domain |
| `packageId` | app.synco.twa | Android package name |
| `startUrl` | /dashboard | Entry point |
| `themeColor` | #1e1553 | Status bar color |
| `minSdkVersion` | 24 | Android 7.0+ |
