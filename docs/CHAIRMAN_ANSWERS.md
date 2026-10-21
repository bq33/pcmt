# PCMT: Answers to Chairman's 8 Questions (2026-10-21)

## 1. API details

- **Login type:** Instagram Login (via the Instagram API use case with Instagram Login, NOT Facebook Login)
- **API version:** v21.0
- **Hostname:** graph.instagram.com
- **List:** `GET /{ig-media-id}/comments` — returns empty data[] (blocked, see Q3)
- **Hide:** `POST /{ig-comment-id}/hide` with `hide=true` — FAILED on a fresh comment (ID 18100494152364466, posted via API 2 minutes prior). Error: code 100, subcode 33, "Unsupported post request. Object with ID does not exist, cannot be loaded due to missing permissions, or does not support this operation." Trace: A1OCsRz3wsLaGdScmg2OgXZ
- **Delete:** `DELETE /{ig-comment-id}` — WORKS. Returns `{"success":true}`. Tested 2026-10-21 on the same fresh comment after hide failed.

## 2. Empty comment array diagnostics

- **Media ID:** 18130694164826510 (photo post, Oct 14 electrician ranking)
- **Test comment:** IG-native, posted by @bqtotheizzo (Brandon's personal account, NOT an app tester) via the Instagram mobile app
- **Posted by:** unrelated user (not app role, not the business account itself)
- **Fetch by ID:** Cannot — we don't have the comment ID because listing returns empty. The API-posted test comment WAS fetchable by its known ID before deletion.
- **comments_count:** Returns 1 (API knows it exists, won't list it)

## 3. Dev vs Live mode

- **Have not tried switching to Live.** App is in Development mode.
- **What prevents Live:** Haven't attempted. The portal shows the app as "In Development" with no explicit blocker message displayed.
- **Webhook subscription:** Toggle exists per Instagram account in the use case setup, currently Off for @craftpath.online.
- **Real webhook received:** No (none configured yet).
- **Account-level vs non-role:** The test comment was from a non-role user (@bqtotheizzo). The API-posted test comment (from the business account itself) WAS visible via API. This suggests the listing filter may be user-based.

## 4. Webhook receiver readiness

- **Signature verification:** Yes, HMAC-SHA256 via X-Hub-Signature-256 (implemented in receiver.py)
- **Retries/idempotency:** NOT yet implemented — needs deduplication by comment ID
- **Prompt injection:** The engine treats comment text as untrusted data (never executes it), but explicit hardening against instruction-in-comment attacks needs review
- **Rate limiting:** NOT yet implemented
- **Token safeguarding:** Config file (needs secure vault in production, currently placeholder)
- **HTTPS endpoint:** NOT yet deployed — code is ready, needs hosting
- **Paths:** ~/workspace/pcmt/webhook/receiver.py, moderation.py, DEPLOY.md

## 5. Engine vs v1.2 integration

- **Currently:** Running a separate parallel implementation (my moderation.py), NOT integrated with the v1.2 Markdown/YAML lexicon
- **Test pass rate:** Not yet measured
- **False positives:** Not yet tested for "mudshark" variants or benign uses
- **Next step:** Integrate the v1.2 lexicon YAML files as the rule source instead of the hardcoded blocklist

## 6. Threads adapter status

- **Status:** Nothing built. Documented limitation only.
- **Proven:** Nothing. Threads API does not support deleting others' replies (per Meta docs).
- **Do NOT label as working.** The capability matrix marks all Threads delete operations as Blocked or Documented-not-tested.

## 7. GitHub repo

- **Exists:** Not yet — building now at ~/workspace/pcmt/github/
- **Controls it:** Brandon (will be under his GitHub)
- **License:** MIT for code (from v1.2 pack), separate content license for lexicon (from v1.2 pack)
- **Safe to publish:** The v1.2 pack is clean (no secrets, no PII scanned). My engine files use placeholder tokens. No private comment logs included. Synthetic demo only.

## 8. Blockers needing Brandon today

| Blocker | Owner | Needed by |
|---------|-------|-----------|
| GitHub repo creation (or access to create under his account) | Brandon | Today |
| License confirmation (MIT ok, or prefer different?) | Brandon | Today |
| App Secret for webhook signature verification | Brandon | When deploying webhooks |
| Decision: publish docs-only alpha if engine isn't fully tested by EOD Oct 22 | Brandon | Oct 22 |

## Summary

The core DELETE capability is proven. The listing gap is real and unexplained. Webhooks are the automation path but need App Review + deployment. The v1.2 pack is clean and ready as the open-source base. Main blocker for tomorrow's deadline is GitHub repo setup.
