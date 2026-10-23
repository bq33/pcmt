#!/usr/bin/env python3
"""PCMT webhook receiver: handles Meta webhook verification and comment events.

Endpoints:
- GET  /webhook  -- Meta verification (hub.mode, hub.challenge, hub.verify_token)
- POST /webhook  -- comment notifications from Instagram

On each comment event: fetch the comment text via API, run the moderation
engine, and act per the configured operating mode. All decisions are logged.
"""
import hashlib
import hmac
import json
import os
import urllib.parse
import urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer

from moderation import load_config, check_comment, api_delete_comment, api_hide_comment

API_HOST = "graph.instagram.com"
LOG_PATH = os.path.join(os.path.dirname(__file__), "moderation.log")


def log_event(entry):
    entry["ts"] = __import__("datetime").datetime.utcnow().isoformat() + "Z"
    line = json.dumps(entry)
    with open(LOG_PATH, "a") as f:
        f.write(line + "\n")
    print(line, flush=True)


def get_comment_text(comment_id, access_token):
    url = (f"https://{API_HOST}/v21.0/{comment_id}"
           f"?fields=id,text,username,timestamp&access_token={urllib.parse.quote(access_token)}")
    with urllib.request.urlopen(url, timeout=30) as resp:
        return json.load(resp)


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Meta webhook verification
        qs = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        mode = qs.get("hub.mode", [""])[0]
        challenge = qs.get("hub.challenge", [""])[0]
        token = qs.get("hub.verify_token", [""])[0]
        config = load_config()
        if mode == "subscribe" and token == config.get("verify_token"):
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(challenge.encode())
            log_event({"event": "webhook_verified"})
        else:
            self.send_response(403)
            self.end_headers()

    def do_POST(self):
        config = load_config()
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)

        # Verify signature
        sig = self.headers.get("X-Hub-Signature-256", "")
        expected = "sha256=" + hmac.new(
            config.get("app_secret", "").encode(), body, hashlib.sha256
        ).hexdigest()
        if not hmac.compare_digest(sig, expected):
            self.send_response(403)
            self.end_headers()
            log_event({"event": "bad_signature"})
            return

        self.send_response(200)
        self.end_headers()

        try:
            payload = json.loads(body)
        except json.JSONDecodeError:
            log_event({"event": "bad_payload"})
            return

        for entry in payload.get("entry", []):
            for change in entry.get("changes", []):
                if change.get("field") != "comments":
                    continue
                value = change.get("value", {})
                comment_id = value.get("id")
                media_id = value.get("media_id")
                if not comment_id:
                    continue
                self.handle_comment(comment_id, media_id, config)

    def handle_comment(self, comment_id, media_id, config):
        token = config.get("access_token", "")
        try:
            comment = get_comment_text(comment_id, token)
        except Exception as e:
            log_event({"event": "fetch_failed", "comment_id": comment_id,
                       "error": str(e)})
            return
        text = comment.get("text", "")
        username = comment.get("username", "")
        action, reason = check_comment(text, username, config)
        log_event({"event": "evaluated", "comment_id": comment_id,
                   "username": username, "action": action, "reason": reason,
                   "text_preview": text[:80]})
        if action == "delete":
            try:
                api_delete_comment(comment_id, token)
                log_event({"event": "deleted", "comment_id": comment_id})
            except Exception as e:
                log_event({"event": "delete_failed", "comment_id": comment_id,
                           "error": str(e)})
        elif action == "hide":
            try:
                api_hide_comment(comment_id, token, hide=True)
                log_event({"event": "hidden", "comment_id": comment_id})
            except Exception as e:
                log_event({"event": "hide_failed", "comment_id": comment_id,
                           "error": str(e)})

    def log_message(self, *args):
        pass  # quiet


if __name__ == "__main__":
    port = int(os.environ.get("PORT", os.environ.get("PCMT_PORT", "8443")))
    server = HTTPServer(("0.0.0.0", port), Handler)
    print(f"PCMT webhook receiver on :{port}")
    server.serve_forever()
