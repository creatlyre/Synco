# Synco — Monetization & Licensing Model

Synco is open-source software with a dual-license model. This document explains what is free, what is paid, and what obligations apply.

## What Is Free (AGPL-3.0)

- The full Synco source code is available under the [GNU Affero General Public License v3.0](LICENSE) (AGPL-3.0).
- Anyone can **self-host Synco for personal or household use** at no cost.
- Community contributions are welcome under AGPL-3.0.
- If you modify and distribute or host Synco, AGPL-3.0 requires you to make your modifications available under the same license (see [AGPL-3.0 Obligations](#agpl-30-obligations-plain-language) below).

## What Is Paid

### Synco Cloud (SaaS)

Hosted by Synco — no server setup needed.

- **Free tier** — Basic household calendar and budget features.
- **Pro tier** — Premium features, priority support, advanced integrations.
- **Family Plus tier** — Everything in Pro, plus extended storage and priority email support.

> Exact pricing and feature gating will be defined at launch. Subscription billing is handled via Stripe or Paddle.

### Self-Hosted Commercial License

A one-time purchase for organizations or advanced users who want to self-host Synco **without AGPL-3.0 obligations**.

- Includes: private Docker images, setup guide, purchase-token validation.
- Perpetual license for the purchased version; updates available via renewal.
- See [COMMERCIAL-LICENSE.md](COMMERCIAL-LICENSE.md) for full commercial terms.

### What Paying Customers Get

| | Synco Cloud (SaaS) | Self-Hosted Commercial |
|---|---|---|
| Managed hosting | ✓ | — (you host) |
| Automatic updates | ✓ | Via renewal |
| Priority support | ✓ (Pro+) | Email support |
| Premium features | ✓ (gated by plan) | All features included |
| AGPL source obligation | N/A (hosted service) | Removed |
| Private Docker images | N/A | ✓ |
| Setup documentation | N/A | ✓ |

## AGPL-3.0 Obligations (Plain Language)

- **Personal use:** If you use Synco as-is for personal or household use, you have no additional obligations beyond the license terms.
- **Modified network service:** If you modify Synco and run it as a network service (e.g., host your own modified version for others), you must make your modified source code available to users of that service under AGPL-3.0.
- **Redistribution:** If you redistribute Synco (modified or unmodified), you must include the AGPL-3.0 license and make source code available.
- **Commercial license removes these obligations.** See [COMMERCIAL-LICENSE.md](COMMERCIAL-LICENSE.md).

> **Note:** This is a plain-language summary for convenience. See the full [AGPL-3.0 text](LICENSE) for authoritative terms.

## Pricing

Pricing details will be published at launch. Check the pricing page (coming soon) for current plans and rates.

## Mobile Access Strategy

Synco provides mobile access through:

1. **Progressive Web App (PWA)** — Install Synco to your home screen from any modern browser. Works on iOS, Android, and desktop. Offline shell with cached assets.
2. **Android Wrapper (TWA)** — A lightweight Android app via Trusted Web Activity for Google Play Store distribution. No native code — Chrome renders the full app.

### Why Not a Native App?

A full native iOS/Android rewrite is **explicitly deferred** until monetization is validated. Rationale:

- PWA + TWA covers 95%+ of mobile use cases (home screen install, fullscreen, offline shell)
- Native development would 3-5x the maintenance burden for a two-person household app
- Users already get phone notifications via Google Calendar sync
- Revenue validation must come before platform expansion

This decision will be revisited after v4.0 proves product-market fit and sustainable revenue.

## FAQ

**Can I use Synco for free?**
Yes. The AGPL-3.0 version is fully functional. Self-host it for your household at no cost.

**Do I need a commercial license to use Synco Cloud?**
No. Synco Cloud is a subscription service. The commercial license is specifically for self-hosting without AGPL-3.0 obligations.

**Can I contribute to Synco?**
Yes. Contributions are accepted under AGPL-3.0.

**What if my company cannot use AGPL software?**
Purchase a commercial license. See [COMMERCIAL-LICENSE.md](COMMERCIAL-LICENSE.md) for details.

**What's the difference between Synco Cloud and self-hosted?**
Synco Cloud is managed hosting with automatic updates and support tiers. Self-hosted means you run Synco on your own infrastructure — the commercial license removes AGPL source disclosure requirements.

---

Copyright (C) 2026 Wojciech. For licensing questions, contact **licensing@synco.app**.
