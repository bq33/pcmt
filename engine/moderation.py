#!/usr/bin/env python3
"""PCMT moderation engine: evaluates Instagram comments against rules.

Operating modes:
- audit_only: flag matches, log them, take no action (default, safe)
- active_hide: hide matching comments via API (requires token)
- active_delete: delete matching comments via API (requires token)

Deletion always requires per-comment approval in the config unless
auto_delete_users lists the commenter explicitly.
"""
import json
import os
import re
import urllib.parse
import urllib.request

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")
API_HOST = "graph.instagram.com"


def load_config():
    with open(CONFIG_PATH) as f:
        return json.load(f)


def check_comment(text, username, config):
    """Return (action, reason) for a comment. Action is one of:
    'allow', 'flag', 'hide', 'delete'."""
    rules = config.get("rules", {})
    mode = config.get("operating_mode", "audit_only")

    # 1. Exact-match blocklist (case-insensitive)
    for term in rules.get("blocked_terms", []):
        if term["term"].lower() in text.lower():
            return escalate(mode, f"blocked term: {term['id']}")

    # 2. Regex patterns
    for pattern in rules.get("blocked_patterns", []):
        if re.search(pattern["regex"], text, re.IGNORECASE):
            return escalate(mode, f"blocked pattern: {pattern['id']}")

    # 3. Known bad actors (auto-delete regardless of content)
    if username.lower() in [u.lower() for u in rules.get("auto_delete_users", [])]:
        return ("delete", f"blocked user: {username}") if mode != "audit_only" else ("flag", f"blocked user: {username}")

    return ("allow", "clean")


def escalate(mode, reason):
    if mode == "audit_only":
        return ("flag", reason)
    if mode == "active_hide":
        return ("hide", reason)
    if mode == "active_delete":
        return ("delete", reason)
    return ("flag", reason)


def api_delete_comment(comment_id, access_token):
    url = f"https://{API_HOST}/v21.0/{comment_id}?access_token={urllib.parse.quote(access_token)}"
    req = urllib.request.Request(url, method="DELETE")
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def api_hide_comment(comment_id, access_token, hide=True):
    url = f"https://{API_HOST}/v21.0/{comment_id}/hide"
    data = urllib.parse.urlencode({
        "hide": str(hide).lower(),
        "access_token": access_token,
    }).encode()
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)
