#!/usr/bin/env python3
"""PCMT synthetic demo: run the moderation engine against fake comments.

All comments below are SYNTHETIC — invented for testing, not from any real user.
Run: python3 demo.py
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "engine"))

from moderation import check_comment

# Synthetic test comments (NOT real — invented for this demo)
SYNTHETIC_COMMENTS = [
    # (username, text, expected_action_in_aggressive_mode)
    ("troll_42", "You are a scam artist, unfollow everyone", "flag"),
    ("spam_bot_99", "Check my bio for free crypto, double your money now", "flag"),
    ("hater_xyz", "This is the worst content I have ever seen, delete your account", "flag"),
    ("genuine_fan", "Love this! Really helpful breakdown of the apprenticeship path.", "allow"),
    ("curious_newcomer", "How long does the electrician apprenticeship take?", "allow"),
    ("promo_spammer", "DM me for OnlyFans collab, hot singles in your area", "flag"),
    ("angry_ex", "I hate you and everything you stand for", "flag"),
    ("supporter_01", "Saved this for later, great stats on wages!", "allow"),
]

def main():
    # Aggressive-mode config for demo (audit_only so nothing is actually deleted)
    config = {
        "operating_mode": "audit_only",
        "rules": {
            "blocked_terms": [
                {"id": "DEMO-001", "term": "scam artist"},
                {"id": "DEMO-002", "term": "OnlyFans"},
                {"id": "DEMO-003", "term": "I hate you"},
                {"id": "DEMO-004", "term": "delete your account"},
            ],
            "blocked_patterns": [
                {"id": "DEMO-RX-001", "regex": r"free crypto.*double your money"},
                {"id": "DEMO-RX-002", "regex": r"hot singles in your area"},
            ],
            "auto_delete_users": [],
        }
    }

    print("PCMT Synthetic Demo (audit_only — no actions taken)")
    print("=" * 60)
    passed = 0
    for username, text, expected in SYNTHETIC_COMMENTS:
        action, reason = check_comment(text, username, config)
        # In audit_only, flag is the expected outcome for blocked content
        want = "flag" if expected == "flag" else "allow"
        status = "PASS" if action == want else "FAIL"
        if status == "PASS":
            passed += 1
        print(f"[{status}] @{username}: {action} ({reason})")
        print(f"       \"{text[:60]}\"")
    print("=" * 60)
    print(f"{passed}/{len(SYNTHETIC_COMMENTS)} passed")

if __name__ == "__main__":
    main()
