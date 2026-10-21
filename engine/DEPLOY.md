# PCMT Webhook Receiver — Deployment

## What this is
An HTTPS endpoint that receives Instagram comment notifications from Meta
in real time, evaluates each comment against your moderation rules, and
acts per the configured mode (audit / hide / delete).

## Files
- `receiver.py` — HTTP server: Meta verification + comment event handling
- `moderation.py` — rule engine (blocklist terms, regex patterns, bad-actor users)
- `config.json` — tokens, mode, rules (NEVER commit real values)
- `moderation.log` — append-only log of every decision

## Deploy steps
1. Host `receiver.py` on a server with a public HTTPS URL
   (any VPS, Railway, Fly.io, etc.). Set `PCMT_PORT` env if needed.
2. Fill in `config.json`:
   - `access_token`: the Instagram User token from the Meta app
   - `app_secret`: the Meta app secret (for signature verification)
   - `verify_token`: any random string you choose (Meta echoes it back)
   - `operating_mode`: start with `audit_only`
3. In the Meta developer portal (PCMT app > Instagram use case >
   API setup > 3. Configure webhooks):
   - Callback URL: `https://your-server/webhook`
   - Verify token: the string from step 2
   - Click Verify and save
4. Enable the Webhook Subscription toggle for @craftpath.online
5. Publish the app (requires App Review for live comment data)

## Operating modes
- `audit_only` (default): flags matches in the log, takes no action.
  Run this first to tune rules without risk.
- `active_hide`: hides matching comments via API.
- `active_delete`: deletes matching comments via API.

## Rules
- `blocked_terms`: exact substrings (case-insensitive), each with an `id`
  and `term`. Example: `{"id": "PCMT-AB-001", "term": "scam"}`
- `blocked_patterns`: regexes for trickier matches.
  Example: `{"id": "PCMT-RX-001", "regex": "d[i1]sc[o0]rd.*nitr[o0]"}`
- `auto_delete_users`: usernames to delete on sight (any mode but audit).

## Log
Every event appends to `moderation.log` as JSON: evaluations, actions
taken, failures. Review it to tune rules before switching out of audit mode.
