# PCMT Capability Matrix (v0.1.0-alpha)

**Status as of 2026-10-21. Proven = tested working. Documented = per Meta docs, not yet tested. Blocked = tested, does not work.**

## Instagram (Graph API v21.0, graph.instagram.com)

| Capability | Status | Notes |
|------------|--------|-------|
| Delete own-account comment | **Proven** | DELETE /{ig-comment-id} returns success:true. Tested 2026-10-21. |
| Post comment via API | **Proven** | POST /{ig-media-id}/comments works. |
| Hide comment via API | **Blocked** | POST /{ig-comment-id}/hide returns code 100, subcode 33 ("does not support this operation"). Tested 2026-10-21 on fresh comment. |
| List comments on media | **Blocked** | GET /{ig-media-id}/comments returns empty data[] even when comments_count=1. Tested across multiple posts 2026-10-21. Polling-based discovery does NOT work. |
| Webhook: comment notifications | **Documented** | `comments` field available in Instagram use case. Requires published app (App Review). Not yet configured. |
| Get comment by ID | **Proven** | GET /{ig-comment-id} works for API-posted comments. |

## Threads

| Capability | Status | Notes |
|------------|--------|-------|
| Delete others' replies | **Blocked** | Threads API does not support deleting other users' replies. Documented limitation. |
| Delete own replies | **Documented** | Per Threads API docs. Not tested. |
| List replies | **Documented** | Per Threads API docs. Not tested. |

## Key architectural implication

Because comment *listing* is blocked, PCMT cannot use polling for discovery.
The supported automation path is **webhooks** (Instagram pushes comment events
in real time) combined with **API delete** for enforcement. Manual mode
(owner spots it, agent deletes it) works today without webhooks.
